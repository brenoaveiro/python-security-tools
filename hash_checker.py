#!/usr/bin/env python3
# calcula e compara hashes de arquivos ou strings

import hashlib
import argparse
import sys
import os

ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512']


def hash_string(text, algo):
    h = hashlib.new(algo)
    h.update(text.encode('utf-8'))
    return h.hexdigest()


def hash_file(filepath, algo):
    if not os.path.isfile(filepath):
        print(f'[!] File not found: {filepath}', file=sys.stderr)
        sys.exit(1)
    h = hashlib.new(algo)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description='Compute and compare MD5/SHA hashes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  python hash_checker.py -f sample.exe --algo sha256\n'
            '  python hash_checker.py -s "password123" --all\n'
            '  python hash_checker.py -f file.bin --compare d8e8fca2dc0f896fd7cb4cb0031ba249'
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='File to hash')
    group.add_argument('-s', '--string', help='String to hash')
    parser.add_argument('--algo', choices=ALGORITHMS, default='sha256', help='Hash algorithm (default: sha256)')
    parser.add_argument('--all', action='store_true', help='Show hashes for all algorithms')
    parser.add_argument('--compare', metavar='HASH', help='Compare result against a known hash')
    args = parser.parse_args()

    compute = (lambda a: hash_file(args.file, a)) if args.file else (lambda a: hash_string(args.string, a))
    label = f'File: {args.file}' if args.file else f'String: "{args.string}"'

    print(f'\n[*] {label}\n')

    if args.all:
        for algo in ALGORITHMS:
            print(f'  {algo.upper():<8}  {compute(algo)}')
    else:
        result = compute(args.algo)
        print(f'  {args.algo.upper():<8}  {result}')
        if args.compare:
            if result.lower() == args.compare.lower().strip():
                print(f'\n[+] MATCH — hashes are identical')
            else:
                print(f'\n[-] NO MATCH')
                print(f'    Expected : {args.compare.lower()}')
                print(f'    Got      : {result}')
    print()


if __name__ == '__main__':
    main()
