import sys

from rich.console import Console
from rich.json import JSON

from src.methods import convert_ros2_response_to_json_s, format_json, handle_input_args

if __name__ == "__main__":

    args, env = handle_input_args(*sys.argv[1:])

    console = Console()
    format_remainder = False
    lines = sys.stdin.readlines()

    for line in lines:
        line = line.strip()
        if not format_remainder:
            print(line, file=sys.stderr)

        if args.format_after_line:
            if line == args.format_after_line:
                format_remainder = True
                continue
        else:
            format_remainder = True

        if format_remainder:
            json_s = convert_ros2_response_to_json_s(line, env)
            console.print(JSON(format_json(json_s)))
            break

