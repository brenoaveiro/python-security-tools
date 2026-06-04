# python-security-tools

Scripts Python que fui escrevendo enquanto estudo segurança ofensiva. Nada complexo — ferramentas pequenas para entender como as coisas funcionam por baixo.

- `port_scanner.py` — scanner TCP simples com threading e banner grabbing opcional
- `hash_checker.py` — calcula e compara hashes MD5/SHA de arquivos ou strings
- `banner_grabber.py` — tenta capturar banners de serviços em portas abertas

Python 3.8+, sem dependências externas.

## Como usar

```bash
# port scanner
python port_scanner.py -t 192.168.1.1 -p 1-1024
python port_scanner.py -t 10.10.10.1 -p 22,80,443 --banners

# hash checker
python hash_checker.py -f arquivo.exe --algo sha256
python hash_checker.py -s "password123" --all
python hash_checker.py -f file.bin --compare d8e8fca2dc0f896fd7cb4cb0031ba249

# banner grabber
python banner_grabber.py -t 192.168.1.1 -p 21,22,80,443
```

Saída do port scanner:

```
[+] 22    /tcp  open  SSH-2.0-OpenSSH_8.9p1 Ubuntu
[+] 80    /tcp  open  Apache/2.4.52
[*] Done — 2 open port(s) found.
```

Alguns serviços não respondem a probes simples (HTTPS precisa de TLS handshake, por exemplo). Banner grabbing deixa o scan mais lento.
