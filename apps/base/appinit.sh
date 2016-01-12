#!/bin/bash
sudo -HEu docker sed -i "s/{{ gtk2_theme }}/`getsetting gtk2_theme`/" /home/docker/.gtkrc-2.0
sudo -HEu docker sed -i "s/{{ gtk2_font }}/`getsetting gtk2_font`/" /home/docker/.gtkrc-2.0
sudo -HEu docker sed -i "s/{{ gtk2_icon_theme }}/`getsetting gtk2_icon_theme`/" /home/docker/.gtkrc-2.0
sudo -HEu docker sed -i "s/{{ gtk2_cursor_theme }}/`getsetting gtk2_cursor_theme`/" /home/docker/.gtkrc-2.0

sudo -HEu docker sed -i "s/{{ gtk3_theme }}/`getsetting gtk3_theme`/" /home/docker/.config/gtk-3.0/settings.ini
sudo -HEu docker sed -i "s/{{ gtk3_font }}/`getsetting gtk3_font`/" /home/docker/.config/gtk-3.0/settings.ini
sudo -HEu docker sed -i "s/{{ gtk3_icon_theme }}/`getsetting gtk3_icon_theme`/" /home/docker/.config/gtk-3.0/settings.ini
sudo -HEu docker sed -i "s/{{ gtk3_cursor_theme }}/`getsetting gtk3_cursor_theme`/" /home/docker/.config/gtk-3.0/settings.ini

sudo -HEu docker sed -i "s/{{ xfwm4_theme }}/`getsetting xfwm4_theme`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml
sudo -HEu docker sed -i "s/{{ xfwm4_font }}/`getsetting xfwm4_font`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml

sudo -HEu docker touch /tmp/.Xauth
sudo -HEu docker xauth -f /tmp/.Xauth add $DISPLAY MIT-MAGIC-COOKIE-1 $XCOOKIE

sudo -HEu docker xfwm4 --daemon --replace
sleep 0.1
sudo -HEu docker xfwm4 --daemon --replace
sleep 0.1
