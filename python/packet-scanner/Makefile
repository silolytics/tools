# Author: John-Philipp Drews
# Credits: John-Philipp Drews
# Email: john.philipp@silolytics.com
# Created: 2024-07-02


# Want to use spaces instead of tabs.
.RECIPEPREFIX := $(.RECIPEPREFIX) $(.RECIPEPREFIX)

# Cleans out generated directory.
clean:
    sudo rm -rf generated/

# Listen for events. Can be re-executed.
# Recorded in individual files per execution
# in generated/.
listen_ip_address = "192.168.1.10"      # Sample IP.
listen_payload_re = '.*'                # Filter packets on payload regex.
listen_port = -1                        # All ports.
packet_listen:
    sudo python3 . --ip-address $(listen_ip_address) --listen-port $(listen_port) --payload-re $(listen_payload_re) --to-file

# For testing. Send packets on defined ip:port.
listen_ip_address = "192.168.1.10"      # Sample IP.
send_sleep = 0.3                        # Wait between packets.
send_port = 12345                       # Sample port.
packet_send:
    sudo python3 . --send-packets --send-sleep $(send_sleep) --send-port $(send_port)

# Replay from file. Previously filtered files are ignored.
# Allows to replay a file previously recorded using `packet_listen`.
# Filtered files are suffixed using `{random_string}-filtered.yaml`.
# Occasionally file names may collide.
replay_payload_re = '.*'
from_file_re = '.*'
packet_replay:
    sudo python3 . --from-file-re $(from_file_re) --payload-re $(replay_payload_re)
