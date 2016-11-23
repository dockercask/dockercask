#!/bin/bash
touch /tmp/.Xauth
xauth -f /tmp/.Xauth add $DISPLAY MIT-MAGIC-COOKIE-1 $XCOOKIE
ln -s -T /home/docker/Docker /home/docker/.config/google-chrome
google-chrome-stable
