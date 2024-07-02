# packet-scanner
Run as sudo.
Ensure requirements added in sudo python version.

```
usage: packet-scanner [-h] [--ip-address IP_ADDRESS] [--listen-port LISTEN_PORT] [--to-file] [--payload-re PAYLOAD_RE] [--from-file-re FROM_FILE_RE] [--send-packets]
                      [--send-sleep SEND_SLEEP] [--send-mac-address SEND_MAC_ADDRESS] [--send-port SEND_PORT]

Scan packets for a given IPv4 address.

options:
  -h, --help            show this help message and exit
  --ip-address IP_ADDRESS
                        Using this IP (v4) (default='192.168.1.10' env_var='PS_IP_ADDRESS').
  --listen-port LISTEN_PORT
                        We'll listing on this port (-1 is all) (default='-1' env_var='PS_LISTEN_PORT').
  --to-file             Write packets as YAML (default='True' env_var='PS_TO_FILE').
  --payload-re PAYLOAD_RE
                        Payload re filter. (default='.*' env_var='PS_PAYLOAD_RE').
  --from-file-re FROM_FILE_RE
                        Read packets from YAML as per previous {{to_file}} output as per regex, sorted as per content of generated/ (default='' env_var='PS_FROM_FILE').
  --send-packets        Send packets on specified {{ip_address}}:{{send_port}} (useful for testing) (default='False' env_var='PS_SEND_PACKETS').
  --send-sleep SEND_SLEEP
                        Sleep in seconds between sending packets (default='1' env_var='PS_SEND_SLEEP').
  --send-mac-address SEND_MAC_ADDRESS
                        MAC address when sending (default='ff:ff:ff:ff:ff:ff' env_var='PS_SEND_MAC_ADDRESS').
  --send-port SEND_PORT
                        Well send in this port (default='12345' env_var='PS_SEND_PORT').
```

For more details on execution see `Makefile`.