#!/bin/bash
appinit
sudo -HEu docker ln -s -T /home/docker/Docker /home/docker/.mozilla
sudo -HEu docker firefox
