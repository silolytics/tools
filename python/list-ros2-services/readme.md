# List ROS2 service details

```
usage: list-ros2-services [-h] [-i INCLUDE_ENDPOINTS_RE] [-s SKIP_ENDPOINTS_RE] [-o OUTPUT_FILE_NAME] [-n NUM_THREADS]

List ros2 services with request/response JSON.

options:
  -h, --help            show this help message and exit
  -i INCLUDE_ENDPOINTS_RE, --include-endpoints-re INCLUDE_ENDPOINTS_RE
                        Service regex to include based on endpoint (default='.*' env_var='PR_I').
  -s SKIP_ENDPOINTS_RE, --skip-endpoints-re SKIP_ENDPOINTS_RE
                        Service regex to skip. Prioritised over inclusion (default='' env_var='PR_S').
  -o OUTPUT_FILE_NAME, --output-file-name OUTPUT_FILE_NAME
                        Write output JSON here (default='services' env_var='PR_O').
  -n NUM_THREADS, --num-threads NUM_THREADS
                        Number of threads to use (default='8' env_var='PR_T').
```

Basically lists all currently active ROS2 services on local system based on `ros2 service list`.

Will then build a JSON to specify request and response structure.

Arrays/sequences are handled as arrays with a single item of the inner type.

So `pkg/msg/Type[]` for service `/my/service` at field `attribute_name` in a response will be represented as:
```
{
    ...
    "_services": {
        "/my/service": {
            "_request": {
                ...
            },
            "_response": {
                "attribute_name": [{
                    "_type": "pkg/msg/Type" 
                    ...
                }],
                ...
            },
            ...
        },
    },
    ...
}
```

Output will be written to output file (as per input args) in `generated/`. The filename will be appended with a timestamp and `.json` extension.

Metadata includes which namespaces where skipped and included (based on provided regexes). Also includes calling argument and relevant env variables at invocation. For any reducible type we nest until we hit irreducible types (e.g. `boolean`, `int`, ...).

You need to have the relevant ROS2 application running locally. With `ros2` in your `PATH`.