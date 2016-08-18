#!/bin/bash
touch /tmp/.Xauth
xauth -f /tmp/.Xauth add $DISPLAY MIT-MAGIC-COOKIE-1 $XCOOKIE

mkdir -p /home/docker/.local/share
mkdir -p /home/docker/Docker/steam
mkdir -p /home/docker/Docker/local
mkdir -p /home/docker/Docker/vulkan
ln -s -T /home/docker/Docker/steam /home/docker/.steam
ln -s -T /home/docker/Docker/local /home/docker/.local/share/Steam
ln -s -T /home/docker/Docker/vulkan /home/docker/.local/share/vulkan

rm /home/docker/.steampath
rm /home/docker/.steampid
rm /home/docker/.steam/steam.pid
rm /home/docker/.steam/steam.pipe
rm /home/docker/.steam/registry.vdf

steam
