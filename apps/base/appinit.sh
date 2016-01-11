#!/bin/bash
sudo -HEu docker sed -i "s/{{ gtk2_theme }}/`jq -r .gtk2_theme base.json`/" /home/docker/.gtkrc-2.0
sudo -HEu docker sed -i "s/{{ gtk2_font }}/`jq -r .gtk2_font base.json`/" /home/docker/.gtkrc-2.0
sudo -HEu docker sed -i "s/{{ gtk2_icon_theme }}/`jq -r .gtk2_icon_theme base.json`/" /home/docker/.gtkrc-2.0
sudo -HEu docker sed -i "s/{{ gtk2_cursor_theme }}/`jq -r .gtk2_cursor_theme base.json`/" /home/docker/.gtkrc-2.0

sudo -HEu docker sed -i "s/{{ gtk3_theme }}/`jq -r .gtk3_theme base.json`/" /home/docker/.config/gtk-3.0/settings.ini
sudo -HEu docker sed -i "s/{{ gtk3_font }}/`jq -r .gtk3_font base.json`/" /home/docker/.config/gtk-3.0/settings.ini
sudo -HEu docker sed -i "s/{{ gtk3_icon_theme }}/`jq -r .gtk3_icon_theme base.json`/" /home/docker/.config/gtk-3.0/settings.ini
sudo -HEu docker sed -i "s/{{ gtk3_cursor_theme }}/`jq -r .gtk3_cursor_theme base.json`/" /home/docker/.config/gtk-3.0/settings.ini

sudo -HEu docker sed -i "s/{{ xfwm4_theme }}/`jq -r .xfwm4_theme base.json`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml
sudo -HEu docker sed -i "s/{{ xfwm4_font }}/`jq -r .xfwm4_font base.json`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml

sudo -HEu docker touch /tmp/.Xauth
sudo -HEu docker xauth -f /tmp/.Xauth add $DISPLAY MIT-MAGIC-COOKIE-1 $XCOOKIE

sudo -HEu docker xfwm4 --daemon --replace
sleep 0.1
sudo -HEu docker xfwm4 --daemon --replace
sleep 0.1
