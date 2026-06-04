#!/usr/bin/env python3
"""
port_scanner.py — Simple TCP port scanner
Part of python-security-tools | Educational use only
"""

import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def scan_port(host, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return port, result == 0
    except socket.error:
        return port, False


def grab_banner(host, port, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        try:
            banner = sock.recv(1024)
        except socket.timeout:
            sock.sendall(b'\r\n')
            banner = sock.recv(1024)
        sock.close()
        return banner.decode('utf-8', errors='ignore').split('\n')[0].strip()[:70]
    except Exception:
        return ''


def parse_ports(port_str):
    ports = []
    for part in port_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return ports


def main():
    parser = argparse.ArgumentParser(
        description='Simple TCP port scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  python port_scanner.py -t 192.168.1.1 -p 1-1024\n'
            '  python port_scanner.py -t 10.10.10.1 -p 22,80,443 --banners'
        )
    )
    parser.add_argument('-t', '--target', required=True, help='Target IP or hostname')
    parser.add_argument('-p', '--ports', default='1-1024', help='Port range (default: 1-1024)')
    parser.add_argument('--timeout', type=float, default=1.0, help='Timeout per port in seconds')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads (default: 100)')
    parser.add_argument('--banners', action='store_true', help='Attempt to grab service banners')
    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f'[!] Could not resolve: {args.target}', file=sys.stderr)
        sys.exit(1)

    ports = parse_ports(args.ports)

    print(f'\n{"="*52}')
    print(f'  Target  : {args.target} ({target_ip})')
    print(f'  Ports   : {args.ports}')
    print(f'  Threads : {args.threads}')
    print(f'  Started : {datetime.now().strftime("%H:%M:%S")}')
    print(f'{"="*52}\n')

    open_ports = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_port, target_ip, p, args.timeout): p for p in ports}
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)

    open_ports.sort()

    if not open_ports:
        print('[-] No open ports found.')
    else:
        for port in open_ports:
            banner = grab_banner(target_ip, port) if args.banners else ''
            banner_str = f'  {banner}' if banner else ''
            print(f'[+] {port:<6}/tcp  open{banner_str}')

    print(f'\n[*] Done — {len(open_ports)} open port(s) found.')


if __name__ == '__main__':
    main()
