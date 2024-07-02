### Pretty JSON responses from ROS2

I found ROS2 responses difficult to read during development on command-line.

Install requirements using:
```
pip3 install -r requirements.txt
```

Set an alias (e.g. in ~/.bashrc) as
```
alias pr='python3 ${path_to_pretty_ros2_responses_dir}'
```

Then pipe ROS2 service calls as:
```
ros2 service call /service/list msgs/srv/ServiceList '{}' | pr
```

Instead of the default response formatting:
```
...
response:
msgs.srv.Srv_Response(loaded=[], backups=[msgs.msg.Msg(id='171', updated_at='2024-05-31 17:14:45', path='/backup/path/1.db3'), msgs.msg.Msg(id='171', updated_at='2024-06-03 11:00:38', path='/backup/path/2.db3')], error=msgs.msg.ErrorMsg(error_code=0, error_msg=''))
```

Yielding formatted response:
```
{
  "loaded": [],
  "backups": [
    {
      "id": "171",
      "updated_at": "2024-05-31 17:14:45",
      "path": "/backup/path/1.db3"
    },
    {
      "id": "171",
      "updated_at": "2024-06-03 11:00:38",
      "path": "/backup/path/2.db3"
    }
  ],
  "error": {
    "error_code": 0,
    "error_msg": ""
  }
}
```

The types can be added using `-i` on the command line or using env variable `PR_I=True|False`. If the value can't be evaluated by `ast.literal_eval()` it's silently ignored. That is, `PR_I=true|false` will be ignored.

Either of
```
ros2 service call /service/list msgs/srv/ServiceList '{}' | pr -i
ros2 service call /service/list msgs/srv/ServiceList '{}' | PR_I=True pr
```
evaluates to:
```
{
  "_type": "msgs.srv.Srv_Response",
  "loaded": [],
  "backups": [
    {
      "_type": "msgs.msg.Msg",
      "id": "171",
      "updated_at": "2024-05-31 17:14:45",
      "path": "/backup/path/1.db3"
    },
    {
      "_type": "msgs.msg.Msg",
      "id": "171",
      "updated_at": "2024-06-03 11:00:38",
      "path": "/backup/path/2.db3"
    }
  ],
  "error": {
    "_type": "msgs.msg.ErrorMsg",
    "error_code": 0,
    "error_msg": ""
  }
}
```

Types are included at the top-level to avoid further nesting of the data, as well as  looking for matching braces in possibly nested JSON.

In case the data already includes key `_type` and the `-i` option is passed, we'll run into a repeated key error. If you want to keep the type prefix, you can rename the type key via env variable `PR_T` and/or option `-t`.

Is there another way to pretty ROS2 messages. Probably. I personally feel JSON should be default.