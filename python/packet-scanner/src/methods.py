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


import argparse
from datetime import datetime
import glob
import json
import os
import random
import re
import string
from time import sleep

import yaml
from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether
from scapy.packet import Raw
from scapy.sendrecv import sendp, sniff

from src.env import ENV, GLOBALS, update_env_from_args


def handle_input_args(*args):
    log = GLOBALS.LOG
    parser = argparse.ArgumentParser(
        prog=GLOBALS.app_name, description='Scan packets for a given IPv4 address.')

    for field_name, field in ENV.__dict__.items():
        try:
            parser.add_argument(
                field.flag_name, default=field.value, help=field.help_str, **field.kwargs)
        except Exception as ex:
            log.error(f"Failed adding field to env: {field_name}")
            raise ex

    parsed_args = parser.parse_args(args=args)
    update_env_from_args(ENV, parsed_args)
    return parsed_args, ENV


def as_filter_string(ip_address, port=None):
    filter_string = f"host {ip_address}"
    if port:
        filter_string += f" and port {port}"
    return filter_string


def packet_received_cb(packet, payload_re, output_file):
    log = GLOBALS.LOG

    summary = packet.summary()
    now = datetime.now()
    payload = ""
    if packet.haslayer(Raw):
        payload = packet[Raw].load.decode()
        if payload_re:
            if not re.match(payload_re, payload):
                log.info(f"Payload didn't match payload_re='{payload_re}' payload'{payload}'")
                return

    to_write = dict(
        time=now.isoformat(),
        summary=summary,
        payload=payload
    )
    json_s = json.dumps(to_write)
    line = f"- {json_s}"
    log.info(line)
    if output_file:
        output_file.write(f"{line}\n")
        output_file.flush()


def random_string(n):
    return ''.join(random.choices(string.hexdigits, k=n)).lower()


def data_from_yaml(yaml_path):
    with open(yaml_path) as f:
        return yaml.safe_load(f)


def make_generated_dir():
    generated_dir = GLOBALS.generated_dir
    os.makedirs(generated_dir, exist_ok=True)


def get_files_sorted(directory, file_re):
    files = glob.glob(os.path.join(directory, '*'))
    files = [f for f in files if os.path.isfile(f) and re.match(file_re, f)]
    files.sort()
    return files


def get_filtered_output_path(file_path):
    return f"{file_path.replace('.yaml', f'-{random_string(8)}-filtered.yaml')}"


def get_output_file_path():
    return os.path.join(
        GLOBALS.generated_dir,
        f"{GLOBALS.packets_yaml_prefix}_{datetime.now().isoformat()}.yaml")


def matches_re(pattern_re, data, log):
    if pattern_re:
        if not re.match(pattern_re, data):
            log.info(f"Data didn't match pattern_re='{pattern_re}' data='{data}'")
            return False
    return True


def dumps_packet(packet, log):
    json_s = json.dumps(packet)
    line = f"- {json_s}"
    log.info(line)
    return line


def write_line_to_file(output_file, line):
    output_file.write(f"{line}\n")
    output_file.flush()


def write_output_file_header(output_file):
    output_file.write(f"{GLOBALS.packet_path}:\n")


def handle_packet_from_file(packet, payload_re, log, output_file=None):
    payload = packet[GLOBALS.payload_path]
    if not matches_re(payload_re, payload, log):
        return
    line = dumps_packet(packet, log)
    if output_file:
        write_line_to_file(output_file, line)


def handle_packets_from_file(from_file_re, payload_re, to_file, log):
    files = get_files_sorted(GLOBALS.generated_dir, from_file_re)

    for file_path in files:
        if file_path.endswith("-filtered.yaml"):
            log.info(f"Skipping filtered file: {file_path}")
            continue
        packets = data_from_yaml(file_path)[GLOBALS.packet_path]
        if not packets:
            continue
        output_path = get_filtered_output_path(file_path)
        log.info(f"Will write to: {output_path}")

        if to_file:
            with open(output_path, "w") as output_file:
                write_output_file_header(output_file)
                for packet in packets:
                    handle_packet_from_file(packet, payload_re, log, output_file)
        else:
            for packet in packets:
                handle_packet_from_file(packet, payload_re, log, output_file)


def handle_send_packets(send_sleep, send_mac, send_ip, send_port, log):
    log.info(f"Will send packets (send_sleep={send_sleep}s): {send_ip}@{send_port or '.*'}")

    while True:
        ether = Ether(dst=send_mac)
        tcp = TCP(dport=send_port)
        ip = IP(dst=send_ip)
        packet = ether / ip / tcp / f"Weight: 123kg {random_string(2)}"
        sendp(packet)
        sleep(send_sleep)


def handle_listen(payload_re, ip_address, port, to_file, log):

    if port < 0:
        port = ""

    log.info(f"Will listen for packets {ip_address}@{port or '.*'}")
    filter_string = as_filter_string(ip_address, port)

    if to_file:
        output_path = get_output_file_path()
        log.info(f"Will write here: {output_path}")
        with open(output_path, "w") as output_file:
            write_output_file_header(output_file)
            sniff(
                filter=filter_string,
                prn=lambda packet: packet_received_cb(packet, payload_re, output_file))
    else:
        sniff(
            filter=filter_string,
            prn=lambda packet: packet_received_cb(packet, payload_re, None))


