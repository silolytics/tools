import argparse
import json
import re
from src.env import ENV, update_env_from_args


REGEX_RESPONSE_TYPES = "[a-zA-Z_.0-9]+\\("


def handle_input_args(*args):
    parser = argparse.ArgumentParser(prog='pretty-ros2-responses', description='Prettify ROS2 responses.')
    parser.add_argument(
        '-i', '--include-types',
        action="store_true",
        default=ENV.include_types.value,
        help=f"Include types as {{type-prefix}} in JSON (default={ENV.include_types.value}).")
    parser.add_argument(
        '-t', '--type-prefix',
        default=ENV.type_prefix.value,
        help=f"Defines {{type-prefix}} (default={ENV.type_prefix.value}).")
    parser.add_argument(
        '-f', '--format-after-line',
        default=ENV.format_after_line.value,
        help=f"Only format content once stripped line {{format-after-line}} was hit (default={ENV.format_after_line})."
    )
    parsed_args = parser.parse_args(args=args)
    update_env_from_args(ENV, parsed_args)
    return parsed_args, ENV


def convert_ros2_response_to_json_s(response_string, env):
    compiled_pattern = re.compile(REGEX_RESPONSE_TYPES)
    matches = compiled_pattern.findall(response_string)
    for match in matches:
        if env.include_types.value:
            # Allows to include type in response. Doing this on
            # the inside means we avoid nesting the structure
            # further, and we get to skip the matching nested
            # braces part.
            response_string = response_string.replace(match, f"dict({env.type_prefix.value}='{match[:-1]}', ")
        else:
            response_string = response_string.replace(match, "dict(")
    if response_string.startswith("("):
        response_string = "dict" + response_string
    response_dict = eval(response_string)
    return json.dumps(response_dict)


def format_json(string):
    d = json.loads(string)
    string = json.dumps(d, indent=2)
    return string
