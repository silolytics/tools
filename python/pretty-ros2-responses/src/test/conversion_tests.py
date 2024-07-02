import pytest

from src.env import ENV
from src.methods import convert_ros2_response_to_json_s as to_json_s
from src.methods import format_json


@pytest.mark.parametrize(
    ("input_s", "output_s_no_types", "output_s_including_types"),
    [
        (
                "()",
                "{}",
                "{}"
        ),
        (
                "(a='')",
                '{"a": ""}',
                '{"a": ""}'
        ),
        (
                "type.a(b=type.b(c=''))",
                '{"b": {"c": ""}}',
                '{"_type": "type.a", "b": {"_type": "type.b", "c": ""}}'
        ),
        (
                "(a=123)",
                '{"a": 123}',
                '{"a": 123}'),
        (
                "type.a(key='value')",
                '{"key": "value"}',
                '{"_type": "type.a", "key": "value"}'
        ),
        (
                "type.a(key='')",
                '{"key": ""}',
                '{"_type": "type.a", "key": ""}'
        ),
        (
                "a.b(x=1, y='2', z=1.0)",
                '{"x": 1, "y": "2", "z": 1.0}',
                '{"_type": "a.b", "x": 1, "y": "2", "z": 1.0}'
        ),
        (
                "a.b(x=c.d(y=123, z='a'))",
                '{"x": {"y": 123, "z": "a"}}',
                '{"_type": "a.b", "x": {"_type": "c.d", "y": 123, "z": "a"}}'
        ),
        (
                "c.d(a=[])",
                '{"a": []}',
                '{"_type": "c.d", "a": []}'
        ),
        (
                "c.d(a=[error.type(code=1, message='failed')])",
                '{"a": [{"code": 1, "message": "failed"}]}',
                '{"_type": "c.d", "a": [{"_type": "error.type", "code": 1, "message": "failed"}]}'
        ),
        (
                "a.b(key=\"Don't do it.\")",
                '{"key": "Don\'t do it."}',
                '{"_type": "a.b", "key": "Don\'t do it."}'
        ),
        (
                "a.b(key='This seems \"odd\".')",
                '{"key": "This seems \\"odd\\"."}',
                '{"_type": "a.b", "key": "This seems \\"odd\\"."}'
        ),
        (
                "a.b(key='Don\\'t this seem \"odd\".')",
                '{"key": "Don\'t this seem \\"odd\\"."}',
                '{"_type": "a.b", "key": "Don\'t this seem \\"odd\\"."}'
        ),
        (
                "msgs.srv.Srv_Response(loaded=[], backups=[msgs.msg.Msg(id='171', updated_at='2024-05-31 17:14:45', "
                "path='/backup/path/1.db3'), msgs.msg.Msg(id='171', updated_at='2024-06-03 11:00:38', "
                "path='/backup/path/2.db3')], error=msgs.msg.ErrorMsg(error_code=0, error_msg=''))",

                '{"loaded": [], "backups": [{"id": "171", "updated_at": "2024-05-31 17:14:45", '
                '"path": "/backup/path/1.db3"}, {"id": "171", "updated_at": "2024-06-03 11:00:38", '
                '"path": "/backup/path/2.db3"}], "error": {"error_code": 0, "error_msg": ""}}',

                '{"_type": "msgs.srv.Srv_Response", "loaded": [], "backups": ['
                '{"_type": "msgs.msg.Msg", "id": "171", "updated_at": "2024-05-31 17:14:45", '
                '"path": "/backup/path/1.db3"}, '
                
                '{"_type": "msgs.msg.Msg", "id": "171", "updated_at": "2024-06-03 11:00:38", '
                '"path": "/backup/path/2.db3"}], '
                '"error": {"_type": "msgs.msg.ErrorMsg", "error_code": 0, "error_msg": ""}}'
        )
    ]
)
class TestConversionAndFormat:

    @staticmethod
    def print_context(*strings, n, context=20):
        i = 0
        ok = True
        for i in range(0, n):
            print(f"{i} ", end="")
            chars = set()
            for string in strings:
                char = string[i]
                chars.add(char)
                print(f"{char} ", end="")
            print()
            if len(chars) > 1:
                ok = False
                break
        if not ok:
            for string in strings:
                print(string[max(0, i - context):min(len(string), i + context)])
            for string in strings:
                format_json(string)

    def check(self, input_s, expected_output_s, env):
        json_s = to_json_s(input_s, env)
        if json_s != expected_output_s:
            self.print_context(json_s, expected_output_s, n=len(json_s))
            raise AssertionError(json_s, expected_output_s)

    def test_conversion_and_format(self, input_s, output_s_no_types, output_s_including_types):
        # Notably, this doesn't check the outer argparse handling.
        # We're sort of assuming that to work. :)
        env = ENV
        env.include_types.value = True
        self.check(input_s, output_s_including_types, env)

        env.include_types.value = False
        self.check(input_s, output_s_no_types, env)

