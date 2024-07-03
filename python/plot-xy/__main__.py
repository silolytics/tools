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

import os
import re
import sys
from datetime import datetime

import matplotlib.pyplot as plt

from src.env import GLOBALS
from src.methods import handle_input_args, \
    plot_from_file_path, progression_from_file_name

if __name__ == '__main__':

    log = GLOBALS.LOG
    start_time = datetime.now()
    log.info(f"Started at {start_time}")

    args, env = handle_input_args(*sys.argv[1:])
    log.debug(env.as_dict_s())

    polygon_dir = env.polygon_dir.value
    highest_progression_only = env.highest_progression_only.value
    polygon_file_re = env.polygon_file_re.value

    polygon_files = os.listdir(polygon_dir)
    polygon_files_filtered = [
        f for f in polygon_files if re.match(polygon_file_re, f)
    ]

    if highest_progression_only:
        polygon_files_d = {}
        max_p = -1
        for f in polygon_files_filtered:
            p = progression_from_file_name(f)
            polygon_files_d.setdefault(p, []).append(f)
            if p > max_p:
                max_p = p

        if max_p < 0:
            raise ValueError("Unexpected: max_p < 0")

        latest = polygon_files_d[max_p]
        latest.sort()

        polygon_files_filtered = latest

    for file_path in polygon_files_filtered:
        plot_from_file_path(os.path.join(polygon_dir, file_path))

    plt.legend()
    plt.show()

