#!/opt/conda/bin/python

from notebook.auth import passwd
import os

config_file = "/root/.jupyter/jupyter_notebook_config.py"

print "Setting password to {}".format(os.environ['PASSWD'])
hashed = passwd(os.environ['PASSWD'])

print "Hashed passwd {}".format(hashed)

with open(config_file, "a") as f:
    line = "c.NotebookApp.password = u'{}'".format(hashed)
    f.write(line)

