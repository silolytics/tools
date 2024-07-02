#!/usr/bin/env python3

"""
Packet-scanner. Listen to packets, write to file. Filter. And replay.
"""

__author__ = "John-Philipp Drews"
__copyright__ = "Copyright 2024, Silolytics"
__credits__ = ["John-Philipp Drews"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "John-Philipp Drews"
__email__ = "john.philipp@silolytics.com"
__status__ = "Prototype"


import sys
from datetime import datetime

from src.env import GLOBALS
from src.methods import handle_input_args, make_generated_dir, handle_send_packets, handle_packets_from_file, \
    handle_listen

if __name__ == '__main__':

    log = GLOBALS.LOG
    make_generated_dir()
    start_time = datetime.now()
    log.info(f"Started at {start_time}")

    args, env = handle_input_args(*sys.argv[1:])
    log.debug(env.as_dict_s())

    if env.from_file_re.value:
        handle_packets_from_file(
            from_file_re=env.from_file_re.value,
            payload_re=env.payload_re.value,
            to_file=env.to_file.value,
            log=log
        )
    elif env.send_packets.value:
        handle_send_packets(
            send_sleep=env.send_sleep.value,
            send_port=env.send_port.value,
            send_mac=env.send_mac_address.value,
            send_ip=env.ip_address.value,
            log=log
        )
    else:
        handle_listen(
            payload_re=env.payload_re.value,
            ip_address=env.ip_address.value,
            port=env.listen_port.value,
            to_file=env.to_file.value,
            log=log
        )

    end_time = datetime.now()
    time_diff = end_time - start_time
    log.info(f"Done at {end_time} (took {time_diff.total_seconds():.3f}s).")
