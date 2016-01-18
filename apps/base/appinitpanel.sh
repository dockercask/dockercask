#!/bin/bash
sed -i "s/{{ gtk2_theme }}/`getsetting gtk2_theme`/" /home/docker/.gtkrc-2.0
sed -i "s/{{ gtk2_font }}/`getsetting gtk2_font`/" /home/docker/.gtkrc-2.0
sed -i "s/{{ gtk2_icon_theme }}/`getsetting gtk2_icon_theme`/" /home/docker/.gtkrc-2.0
sed -i "s/{{ gtk2_cursor_theme }}/`getsetting gtk2_cursor_theme`/" /home/docker/.gtkrc-2.0

sed -i "s/{{ gtk3_theme }}/`getsetting gtk3_theme`/" /home/docker/.config/gtk-3.0/settings.ini
sed -i "s/{{ gtk3_font }}/`getsetting gtk3_font`/" /home/docker/.config/gtk-3.0/settings.ini
sed -i "s/{{ gtk3_icon_theme }}/`getsetting gtk3_icon_theme`/" /home/docker/.config/gtk-3.0/settings.ini
sed -i "s/{{ gtk3_cursor_theme }}/`getsetting gtk3_cursor_theme`/" /home/docker/.config/gtk-3.0/settings.ini

sed -i "s/{{ xfwm4_theme }}/`getsetting xfwm4_theme`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml
sed -i "s/{{ xfwm4_font }}/`getsetting xfwm4_font`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml

sed -i "s/{{ gtk2_theme }}/`getsetting gtk2_theme`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml
sed -i "s/{{ gtk2_icon_theme }}/`getsetting gtk2_icon_theme`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml
sed -i "s/{{ gtk2_font }}/`getsetting gtk2_font`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml
sed -i "s/{{ gtk2_cursor_theme }}/`getsetting gtk2_cursor_theme`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml
sed -i "s/{{ dpi }}/`getsetting dpi`/" /home/docker/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml

touch /tmp/.Xauth
xauth -f /tmp/.Xauth add $DISPLAY MIT-MAGIC-COOKIE-1 $XCOOKIE

startxfce4&
sleep 0.25
