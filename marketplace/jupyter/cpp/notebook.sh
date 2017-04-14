#!/bin/bash

# Set C++ env var
export PATH="$PATH:/cling_2017-04-12_ubuntu14/bin"

# Set notebook password
jupyter notebook --generate-config --allow-root
python /root/scripts/setpasswd.py

# Launch notebook
/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser --allow-root
