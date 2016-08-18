FROM dockercask/base
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN pacman -S --noconfirm nvidia nvidia-libgl opencl-nvidia lib32-nvidia-libgl

# RUN aurget cairo-ubuntu
# RUN pacman -U --noconfirm /aur/cairo-ubuntu*.pkg.tar.xz

# RUN aurget freetype2-ubuntu
# RUN pacman -Rdd --noconfirm freetype2
# RUN pacman -U --noconfirm /aur/freetype2-ubuntu*.pkg.tar.xz

# RUN aurget fontconfig-ubuntu
# RUN pacman -Rdd --noconfirm fontconfig
# RUN pacman -U --noconfirm /aur/fontconfig-ubuntu*.pkg.tar.xz

# RUN aurget ubuntu-themes
# RUN pacman -U --noconfirm /aur/ubuntu-themes*.pkg.tar.xz

# RUN rm -rf /aur

RUN wget https://github.com/dockercask/packages/raw/master/cairo-ubuntu-1.14.2-1-x86_64.pkg.tar.xz
RUN pacman -U --noconfirm /cairo-ubuntu-1.14.2-1-x86_64.pkg.tar.xz
RUN rm -f /cairo-ubuntu-1.14.2-1-x86_64.pkg.tar.xz

RUN wget https://github.com/dockercask/packages/raw/master/freetype2-ubuntu-2.6.1-1-x86_64.pkg.tar.xz
RUN pacman -Rdd --noconfirm freetype2
RUN pacman -U --noconfirm /freetype2-ubuntu-2.6.1-1-x86_64.pkg.tar.xz
RUN rm -f /freetype2-ubuntu-2.6.1-1-x86_64.pkg.tar.xz

RUN wget https://github.com/dockercask/packages/raw/master/fontconfig-ubuntu-2.11.94-1-x86_64.pkg.tar.xz
RUN pacman -Rdd --noconfirm fontconfig
RUN pacman -U --noconfirm /fontconfig-ubuntu-2.11.94-1-x86_64.pkg.tar.xz
RUN rm -f /fontconfig-ubuntu-2.11.94-1-x86_64.pkg.tar.xz

RUN wget https://github.com/dockercask/packages/raw/master/ubuntu-themes-14.04.16.04.20160415-1-any.pkg.tar.xz
RUN pacman -Udd --noconfirm /ubuntu-themes-14.04.16.04.20160415-1-any.pkg.tar.xz
RUN rm -f /ubuntu-themes-14.04.16.04.20160415-1-any.pkg.tar.xz

RUN pacman -S --noconfirm xorg-xauth xfwm4 xfce4-panel xfce4-session xfce4-notifyd xfce4-settings lxappearance numix-themes gtk-engines gtk-engine-aurora gtk-engine-murrine human-icon-theme xcursor-vanilla-dmz
