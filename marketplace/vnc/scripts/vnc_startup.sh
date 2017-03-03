#!/bin/bash


#resolve_vnc_connection
VNC_IP=$(ip addr show eth0 | grep -Po 'inet \K[\d.]+')
PORTS=${PORTS:-1}


##change vnc password
echo "change vnc password!"
(echo $VNC_PWD && echo $VNC_PWD) | vncpasswd

rm -f /tmp/.X*

for (( c=1; c<=$PORTS; c++ ))
do

VNC_PORT="590"$c
NO_VNC_PORT="690"$c
echo $VNC_PORT


##start vncserver and noVNC webclient
$NO_VNC_HOME/utils/launch.sh --vnc $VNC_IP:$VNC_PORT --listen $NO_VNC_PORT &
vncserver -kill :$c
vncserver :$c -depth $VNC_COL_DEPTH -geometry $VNC_RESOLUTION

export  DISPLAY=:$c
echo $DISPLAY

startxfce4 &
sleep 1

##log connect options
echo -e "\n------------------ VNC environment started ------------------"
echo -e "\nVNCSERVER started on DISPLAY= $c \n\t=> connect via VNC viewer with $VNC_IP:$VNC_PORT"
echo -e "\nnoVNC HTML client started:\n\t=> connect via http://$VNC_IP:$NO_VNC_PORT/vnc_auto.html?password=..."
done

while true; do sleep 1; done


