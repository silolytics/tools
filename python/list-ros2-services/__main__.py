#!/usr/bin/env python3

"""
List available ROS2 services.

Includes nested request/response type definitions.
Writes to file in JSON.
"""

__author__ = "John-Philipp Drews"
__copyright__ = "Copyright 2024, Silolytics"
__credits__ = ["John-Philipp Drews"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "John-Philipp Drews"
__email__ = "john.philipp@silolytics.com"
__status__ = "Prototype"


import logging
import re
import sys
import os
from datetime import datetime
from multiprocessing import Pool

from src.methods import ros2_list_available_srvs, set_up_output_dict, \
    handle_srv, handle_output, handle_input_args

log = logging.getLogger("list-ros2-services")
logging.basicConfig(level=logging.INFO)


GENERATED_DIR = "generated"

if __name__ == '__main__':
    start_time = datetime.now()
    log.info(f"Started at {start_time}")

    os.makedirs(GENERATED_DIR, exist_ok=True)
    args, env = handle_input_args(*sys.argv[1:])
    log.info(env.as_dict_s())

    ros2_available_srvs = ros2_list_available_srvs()
    log.info(f"Found {len(ros2_available_srvs)} services.")

    output_dict, srv_definitions, ns_skipped, ns_loaded = set_up_output_dict(env, *sys.argv[1:])

    pool = Pool(processes=args.num_threads)
    load_srvs = []
    results = {}
    for srv_name in ros2_available_srvs:
        if not srv_name:
            continue

        if args.skip_endpoints_re and re.match(args.skip_endpoints_re, srv_name):
            log.debug(f"Will skip service: {srv_name}")
            ns_skipped.append(srv_name)
            continue

        if args.include_endpoints_re and re.match(args.include_endpoints_re, srv_name):
            log.info(f"Will load service: {srv_name}")
            load_srvs.append(srv_name)
        else:
            log.debug(f"Skipping service: {srv_name}")
            ns_skipped.append(srv_name)

    total_srvs = len(load_srvs)
    for (i, srv_name) in enumerate(load_srvs):
        ns_loaded.append(srv_name)
        result = pool.apply_async(handle_srv, (total_srvs, i + 1, srv_name))
        results[srv_name] = result

    for srv_name, result in results.items():
        srv_definitions[srv_name] = result.get()

    pool.close()
    pool.join()

    end_time = datetime.now()
    time_diff = end_time - start_time
    output_path = os.path.join(GENERATED_DIR, f"{args.output_file_name}_{end_time.isoformat()}.json")
    handle_output(output_dict, output_path)
    log.info(f"Done at {end_time} (took {time_diff.total_seconds():.3f}s).")
