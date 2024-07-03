# Author: John-Philipp Drews
# Credits: John-Philipp Drews
# Email: john.philipp@silolytics.com
# Created: 2024-07-02


# Want to use spaces instead of tabs.
.RECIPEPREFIX := $(.RECIPEPREFIX) $(.RECIPEPREFIX)

polygon_dir = "../../../src/polygons"
polygon_file_re = ".*"
plot:
    python3 . --polygon-dir $(polygon_dir) --polygon-file-re $(polygon_file_re)

plot-highest-progression:
    python3 . --polygon-dir $(polygon_dir) --polygon-file-re $(polygon_file_re) --highest-progression-only
