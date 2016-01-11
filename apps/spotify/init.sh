#!/bin/bash
appinit
sudo -HEu docker ln -s -T /home/docker/Docker /home/docker/.config/spotify
sudo -HEu docker spotify
