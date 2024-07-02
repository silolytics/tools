# Author: John-Philipp Drews
# Credits: John-Philipp Drews
# Email: john.philipp@silolytics.com
# Created: 2024-07-02


# Want to use spaces instead of tabs.
.RECIPEPREFIX := $(.RECIPEPREFIX) $(.RECIPEPREFIX)

# Cleans out generated directory.
clean:
    rm -rf generated/

include_endpoints_re = '.*'
skip_endpoints_re = ''
output_file_name = 'services'
num_threads = 8
list_services:
    python3 . -i $(include_endpoints_re) -s $(skip_endpoints_re) -o $(output_file_name) -n $(num_threads)
