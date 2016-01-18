#!/bin/bash
appinitpanel
ln -s -T /home/docker/Docker /home/docker/.config/google-chrome
google-chrome-stable --no-sandbox --disable-gpu --disable-flash-3d
