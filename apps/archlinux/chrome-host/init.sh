#!/bin/bash
touch /tmp/.Xauth
xauth -f /tmp/.Xauth add $DISPLAY MIT-MAGIC-COOKIE-1 $XCOOKIE
google-chrome-stable
