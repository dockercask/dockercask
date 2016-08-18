#!/bin/bash
appinitpanel
ln -s -T /home/docker/Docker /home/docker/.config/chromium
chromium-browser --no-sandbox --disable-gpu --disable-flash-3d
