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


import ast
import json
import os
import logging
import copy


APP_NAME = "plot-xy"
LOG = logging.getLogger(APP_NAME)
logging.basicConfig(level=logging.INFO)


class Globals:
    yaml_data_key = "data"
    generated_dir = "generated"
    app_name = APP_NAME
    LOG = LOG


GLOBALS = Globals()


class Field:
    def __init__(self, field_name: str, env_var_name: str, value, help_str: str, **kwargs):
        self.env_var_name = env_var_name
        self.field_name = field_name
        self.flag_name = f"--{field_name.replace('_', '-')}"
        self.value = value
        self.help_str = f"{help_str.strip()} ({self.default_env_var_string()})."
        self.kwargs = kwargs or {}

    def default_env_var_string(self):
        return f"default='{self.value}' env_var='{self.env_var_name}'"

    def as_dict(self):
        d = dict()
        for key, value in self.__dict__.items():
            if key == "kwargs" and "type" in value:
                value = copy.deepcopy(value)
                d.setdefault(key, {})["type"] = value["type"].__name__
            elif hasattr(value, "__dict__"):
                d[key] = value.__dict__
            else:
                d[key] = value
        return d


FIELD_DEFINITIONS = [
    Field(
        "polygon_dir",
        "PX_POLYGON_DIR",
        "polygons",
        "Directory with polygon files",
    ),
    Field(
        "polygon_file_re",
        "PX_POLYGON_FILE_RE",
        ".*",
        "Filter polygon files based on regex",
    ),
    Field(
        "highest_progression_only",
        "PX_LATEST_P_ONLY",
        False,
        "Only use latest set based on {{progression}} for all leaf sizes",
        action="store_true"
    ),
]


class Fields:

    def as_dict(self):
        d = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, Field):
                d[key] = value.as_dict()
            else:
                d[key] = value.__dict__
        return d

    def as_dict_s(self):
        return json.dumps(self.as_dict(), indent=2)


OS_ENV = os.environ
ENV = Fields()
for field in FIELD_DEFINITIONS:
    ENV.__dict__[field.field_name] = field
    if field.env_var_name in OS_ENV:
        try:
            env_value = OS_ENV[field.env_var_name]
            try:
                field.value = ast.literal_eval(env_value)
            except ValueError:
                field.value = env_value
        except KeyError:
            pass


def update_env_from_args(env, args):
    for field_name, env_field in env.__dict__.items():
        if hasattr(args, field_name):
            env_field.value = getattr(args, field_name)



