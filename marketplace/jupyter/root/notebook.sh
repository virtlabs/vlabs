#!/bin/bash

# Prepare ROOT env
. /RT/root/bin/thisroot.sh

# Set notebook password
./setpasswd.py

# Launch notebook
/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser
