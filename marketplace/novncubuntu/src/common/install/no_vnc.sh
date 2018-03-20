#!/usr/bin/env bash
### every exit != 0 fails the script
set -e

echo "Install noVNC - HTML5 based VNC viewer"

mkdir -p $NO_VNC_HOME/utils/websockify 
#####wget -qO- https://github.com/novnc/noVNC/archive/v1.0.0-testing.2.tar.gz | tar xz --strip 1 -C $NO_VNC_HOME
wget -qO- https://github.com/novnc/noVNC/archive/v1.0.0.tar.gz | tar xz --strip 1 -C $NO_VNC_HOME
wget -qO- https://github.com/novnc/websockify/archive/v0.8.0.tar.gz | tar xz --strip 1 -C $NO_VNC_HOME/utils/websockify
chmod +x -v $NO_VNC_HOME/utils/*.sh
echo "create index.html to forward automatically to vnc_auto.html"
ln -s $NO_VNC_HOME/vnc_auto.html $NO_VNC_HOME/index.html
