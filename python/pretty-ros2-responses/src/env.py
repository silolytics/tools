import ast
import os


class Field:
    def __init__(self, field_name: str, env_var_name: str, value):
        self.field_name = field_name
        self.env_var_name = env_var_name
        self.value = value


FIELD_DEFINITIONS = [
    Field("include_types", "PR_I", False),
    Field("type_prefix", "PR_T", "_type"),
    Field("format_after_line", "PR_F", "response:")
]


class Fields:
    pass


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



