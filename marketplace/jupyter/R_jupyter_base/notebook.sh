#!/bin/bash

# Set notebook password
jupyter notebook --generate-config --allow-root
python /root/scripts/setpasswd.py

# Launch notebook
/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser --allow-root
