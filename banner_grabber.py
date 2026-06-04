#!/usr/bin/env python3
"""
banner_grabber.py — Grab service banners from open ports
Part of python-security-tools | Educational use only
"""

import socket
import argparse
import sys


def grab_banner(host, port, timeout=3):
    """Connect to host:port and attempt to read a service banner."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))

        # Some services send a banner immediately on connect
        try:
            data = sock.recv(1024)
            if data:
                sock.close()
                return data.decode('utf-8', errors='ignore').strip()
        except socket.timeout:
            pass

        # Others need a small probe
        sock.sendall(b'\r\n')
        try:
            data = sock.recv(1024)
            sock.close()
            return data.decode('utf-8', errors='ignore').strip() if data else None
        except socket.timeout:
            sock.close()
            return None

    except (ConnectionRefusedError, socket.timeout, OSError):
        return None


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
        description='Grab service banners from open ports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  python banner_grabber.py -t 192.168.1.1 -p 21,22,80,443\n'
            '  python banner_grabber.py -t 10.10.10.1 -p 1-1024 --timeout 2'
        )
    )
    parser.add_argument('-t', '--target', required=True, help='Target IP or hostname')
    parser.add_argument('-p', '--ports', required=True, help='Ports to check (e.g. 22,80,443)')
    parser.add_argument('--timeout', type=float, default=3.0, help='Timeout per connection in seconds')
    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f'[!] Could not resolve: {args.target}', file=sys.stderr)
        sys.exit(1)

    ports = parse_ports(args.ports)

    print(f'\n[*] Banner grabbing — {args.target} ({target_ip})')
    print(f'[*] Checking {len(ports)} port(s)...\n')

    found = 0
    for port in ports:
        banner = grab_banner(target_ip, port, args.timeout)
        if banner:
            first_line = banner.split('\n')[0][:80]
            print(f'[+] {port:<6}/tcp  {first_line}')
            found += 1
        else:
            print(f'[-] {port:<6}/tcp  no response')

    print(f'\n[*] Done — {found} banner(s) captured.')


if __name__ == '__main__':
    main()
