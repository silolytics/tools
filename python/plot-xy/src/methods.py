"""
Plot-xy. Plot from yaml xy files.
t: $timestamp
data:
    - {x: $x, y: $y}
    ...
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
import os
import re

import yaml
from matplotlib import pyplot as plt


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


def load_yaml_gen(file_path):
    with open(file_path) as f:
        data_raw = f.read()
    return yaml.safe_load_all(data_raw)


def load_yamls_from_gen(yaml_gen, skip=0):
    yamls = []
    skipped = 0
    for yaml_data in yaml_gen:
        if skip > 0 and skipped < skip:
            skipped += 1
            continue
        skipped = 0
        yamls.append(yaml_data)
    return yamls


def load_latest_yaml(file_path):
    yaml_gen = load_yaml_gen(file_path)
    yamls = load_yamls_from_gen(yaml_gen)
    return yamls[-1]


def plot_with_label(points, label, plt_):
    xs = []
    ys = []
    for point in points:
        xs.append(point["x"])
        ys.append(point["y"])
    plt.plot(xs, ys, label=label)


def label_from_file_name(file_name):
    return file_name


def plot_yaml_data(file_name, yaml_data):
    label = label_from_file_name(file_name)
    xy_data = yaml_data["data"]
    t = yaml_data["t"]
    plot_with_label(xy_data, f"{label}@t={t}", plt)


def plot_from_file_path(file_path):
    file_name = os.path.basename(file_path)
    yaml_data = load_latest_yaml(file_path)
    plot_yaml_data(file_name, yaml_data)


def progression_from_file_name(file_name):
    pattern = re.compile(".*p=([^_]+).*")
    groups = pattern.match(file_name).groups()
    if len(groups) == 0:
        raise ValueError(f"Unexpected: no progression found for file_name={file_name}")
    return float(groups[0])
