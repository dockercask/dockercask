#!/bin/bash
appinitpanel
sudo -HEu docker ln -s -T /home/docker/Docker /home/docker/.config/google-chrome
sudo -HEu docker google-chrome-stable --no-sandbox --disable-gpu --disable-flash-3d
