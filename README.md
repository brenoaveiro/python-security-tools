# python-security-tools

Small Python scripts for security automation and learning. Built while studying offensive security fundamentals.

## Tools

| Script | Description |
|--------|-------------|
| `port_scanner.py` | Multi-threaded TCP port scanner with optional banner grabbing |
| `hash_checker.py` | Compute and compare MD5/SHA hashes for files and strings |
| `banner_grabber.py` | Grab service banners from open ports |

## Requirements

- Python 3.8+
- No external dependencies (standard library only)

## Usage

### Port Scanner

```bash
# Scan common ports
python port_scanner.py -t 192.168.1.1 -p 1-1024

# Specific ports with banner grabbing
python port_scanner.py -t 10.10.10.1 -p 22,80,443,8080 --banners

# Fast scan with more threads
python port_scanner.py -t 192.168.1.1 -p 1-65535 --threads 200 --timeout 0.5
```

```
====================================================
  Target  : 10.10.10.1 (10.10.10.1)
  Ports   : 22,80,443
  Threads : 100
  Started : 14:32:01
====================================================

[+] 22    /tcp  open  OpenSSH 8.9p1 Ubuntu
[+] 80    /tcp  open  Apache/2.4.52
[+] 443   /tcp  open

[*] Done — 3 open port(s) found.
```

### Hash Checker

```bash
# Hash a file
python hash_checker.py -f sample.exe --algo sha256

# Hash a string with all algorithms
python hash_checker.py -s "password123" --all

# Compare against a known hash
python hash_checker.py -f file.bin --compare d8e8fca2dc0f896fd7cb4cb0031ba249
```

```
[*] String: "password123"

  MD5       482c811da5d5b4bc6d497ffa98491e38
  SHA1      cbfdac6008f9cab4083784cbd1874f76618d2a97
  SHA256    ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
  SHA512    bed4efa1d4fdbd954bd3705d6a2a78270ec9a52ecfbfb010c61862af5c76af1761ffeb1aef6aca1bf5d02b3781aa854fabd2b69c790de74e17ecfec3cb6ac4bf
```

### Banner Grabber

```bash
python banner_grabber.py -t 192.168.1.1 -p 21,22,80,443
```

```
[*] Banner grabbing — 192.168.1.1 (192.168.1.1)
[*] Checking 4 port(s)...

[+] 21    /tcp  220 ProFTPD Server (ProFTPD) [192.168.1.1]
[+] 22    /tcp  SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1
[-] 80    /tcp  no response
[+] 443   /tcp  HTTP/1.1 400 Bad Request

[*] Done — 3 banner(s) captured.
```

## Notes

- Scanner uses threading — adjust `--threads` based on your network
- Banner grabbing adds extra time per port
- Some services won't respond to basic probes (e.g. HTTPS needs TLS handshake)

## Disclaimer

> For educational and authorized testing only.
> Do not run against systems you don't own or have explicit permission to test.

## License

MIT
