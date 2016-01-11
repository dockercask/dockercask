#!/bin/bash
appinit
sudo -HEu docker ln -s -T /home/docker/Docker /home/docker/.thunderbird
sudo -HEu docker thunderbird
