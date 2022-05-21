#!/bin/sh

#start pigpiod daemon, use -t 0 if you do *not* use the headphonejack for audio
sudo pigpiod -t 1

# give the daemon a moment to start up before issuing the sbpd command
sleep 1

# load uinput module, then set the permission to group writable, so you don't need to run sbpd with root permissions
sudo modprobe uinput
sudo chmod g+w /dev/uinput

# issue the sbpd command
sbpd b,27,PLAY,2 b,26,NEXT,2 b,20,PREV,2 e,5,6,VOLU,2
