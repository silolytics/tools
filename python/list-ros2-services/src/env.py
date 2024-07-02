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


import ast
import json
import os


class Field:
    def __init__(self, field_name: str, env_var_name: str, value):
        self.field_name = field_name
        self.env_var_name = env_var_name
        self.value = value


FIELD_DEFINITIONS = [
    Field("include_endpoints_re", "PR_I", ".*"),
    Field("skip_endpoints_re", "PR_S", ""),
    Field("output_file_name", "PR_O", "services"),
    Field("num_threads", "PR_T", 8)
]


class Fields:
    pass

    def as_dict(self):
        d = dict()
        for key, value in self.__dict__.items():
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



