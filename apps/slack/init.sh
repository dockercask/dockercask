#!/bin/bash
appinitpanel
sudo -HEu docker ln -s -T /home/docker/Docker /home/docker/.config/Slack
sudo -HEu docker slack
