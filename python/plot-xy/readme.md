# plot-xy

```
usage: plot-xy [-h] [--polygon-dir POLYGON_DIR] [--polygon-file-re POLYGON_FILE_RE] [--highest-progression-only]

Scan packets for a given IPv4 address.

options:
  -h, --help            show this help message and exit
  --polygon-dir POLYGON_DIR
                        Directory with polygon files (default='polygons' env_var='PX_POLYGON_DIR').
  --polygon-file-re POLYGON_FILE_RE
                        Filter polygon files based on regex (default='.*' env_var='PX_POLYGON_FILE_RE').
  --highest-progression-only
                        Only use latest set based on {{progression}} for all leaf sizes (default='False' env_var='PX_LATEST_P_ONLY').
```

Plot polygons using matplotlib from YAML.

Expected YAML data structure:
```
t: ${timestamp: float}
data:
    - {x: ${x_coord: float}, y: ${y_coord: float}},
    ...
```

If multiple files are found in `polygon_dir`, all will be plotted on the same plot.

For `--highest-progression-only` we expect a parameter `..._p=${x: float}_...` in the filename to determine progression.

See `Makefile` for further usage.