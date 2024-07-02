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


import argparse
import json

import subprocess
import logging
from rosidl_runtime_py.utilities import get_service, get_message

from src.env import ENV, update_env_from_args


log = logging.getLogger("list-ros2-services")
logging.basicConfig(level=logging.INFO)


def handle_input_args(*args):
    parser = argparse.ArgumentParser(
        prog='list-ros2-services', description='List ros2 services with request/response JSON.')
    env_field = ENV.include_endpoints_re
    parser.add_argument(
        '-i', '--include-endpoints-re',
        default=env_field.value,
        help=f"Service regex to include based on endpoint "
             f"(default='{env_field.value}' env_var='{env_field.env_var_name}').")
    env_field = ENV.skip_endpoints_re
    parser.add_argument(
        '-s', '--skip-endpoints-re',
        default=env_field.value,
        help=f"Service regex to skip. Prioritised over inclusion "
             f"(default='{env_field.value}' env_var='{env_field.env_var_name}').")
    env_field = ENV.output_file_name
    parser.add_argument(
        '-o', '--output-file-name',
        default=env_field.value,
        help=f"Write output JSON here "
             f"(default='{env_field.value}' env_var='{env_field.env_var_name}').")
    env_field = ENV.num_threads
    parser.add_argument(
        '-n', '--num-threads',
        default=env_field.value,
        type=int,
        help=f"Number of threads to use "
             f"(default='{env_field.value}' env_var='{env_field.env_var_name}').")

    parsed_args = parser.parse_args(args=args)
    update_env_from_args(ENV, parsed_args)
    return parsed_args, ENV


def run_process(command_args):
    log.debug(f"Running command: {command_args}")
    p = subprocess.Popen(
        command_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, _ = p.communicate()
    response = stdout.decode().split("\n")
    log.debug(f"Returned: {response}")
    return response


# Found rclpy.node.Node to be unreliable in terms of the
# services it returned. Numbers varied wildly on invocation.
# Version (as per pip freeze): rclpy==3.3.13
# The following is easier and works reliably.
def ros2_list_available_srvs():
    return run_process(["ros2", "service", "list"])


def ros2_get_service_type(service_name):
    return run_process(["ros2", "service", "type", service_name])[0]


def build_srv(srv_name, srv_meta_ref):
    log.debug(f"Building service: {srv_name}")
    srv_dict = {}
    add_request_response(srv_dict, "_request", srv_meta_ref.Request)
    add_request_response(srv_dict, "_response", srv_meta_ref.Response)
    return srv_dict


def add_request_response(containing_dict, key, meta_ref):
    log.debug(f"Adding request_response: {key}")
    attribute_dict = containing_dict.setdefault(key, {})
    field_and_field_types = meta_ref.get_fields_and_field_types()
    for attribute_name, attribute_meta_ref in field_and_field_types.items():
        populate_types(attribute_dict, attribute_name, attribute_meta_ref)


def populate_types(containing_dict, attribute_name, meta_ref):
    log.debug(f"Populating inner types: {attribute_name}")
    is_array = False
    if meta_ref.startswith("sequence<"):
        is_array = True
        meta_ref = meta_ref[9:-1]
    if "/" in meta_ref:
        # We nest.
        log.debug(f"Nesting into meta_ref: {meta_ref}")
        if is_array:
            container = containing_dict.setdefault(attribute_name, [{"_type": meta_ref}])[0]
        else:
            container = containing_dict.setdefault(attribute_name, {"_type": meta_ref})
        if "," in meta_ref:
            meta_ref = meta_ref.split(",")[0]
            log.debug(f"Corrected meta_ref to: {meta_ref}")
        inner_msg = get_message(meta_ref)
        inner_fields = inner_msg.get_fields_and_field_types()
        for inner_name, inner_meta_ref in inner_fields.items():
            populate_types(container, inner_name, inner_meta_ref)
    else:
        log.debug(f"Adding type: ({attribute_name}: {meta_ref})")
        containing_dict[attribute_name] = meta_ref


def set_up_output_dict(env, *sys_args):
    output_dict = dict()
    metadata = output_dict.setdefault("_metadata", {})
    metadata["_sys_args"] = sys_args
    metadata["_env"] = env.as_dict()
    srv_definitions = output_dict.setdefault("_services", {})
    ns_skipped = metadata.setdefault("_namespaces_skipped", [])
    ns_loaded = metadata.setdefault("_namespaces_loaded", [])
    return output_dict, srv_definitions, ns_skipped, ns_loaded


def handle_srv(total_srvs, srv_i, srv_name):
    log.info(f"Handling service ({srv_i}/{total_srvs}): {srv_name}")
    srv_type = ros2_get_service_type(srv_name)
    srv_meta_ref = get_service(srv_type)
    return build_srv(srv_name, srv_meta_ref)


def handle_output(output_dict, output_path):
    json_s = json.dumps(output_dict, indent=2)
    with open(output_path, "w") as output_file_name:
        output_file_name.write(json_s)
    log.info(f"Written to: {output_path}")
    log.debug(f"JSON: {json_s}")


