#!/bin/bash
appinit
sudo -HEu docker ln -s -T /home/docker/Docker /home/docker/.config/chromium
sudo -HEu docker chromium --no-sandbox --disable-gpu --disable-flash-3d
