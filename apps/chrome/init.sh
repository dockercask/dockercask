#!/bin/bash
appinit
sudo -HEu docker ln -s -T /home/docker/Docker /home/docker/.config/google-chrome
sudo -HEu docker google-chrome-stable --no-sandbox