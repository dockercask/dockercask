FROM dockercask/base
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN pacman -S --noconfirm xf86-video-intel mesa-libgl opencl-mesa lib32-mesa-libgl

RUN aurget cairo-ubuntu
RUN pacman -Rdd --noconfirm cairo
RUN pacman -U --noconfirm /aur/cairo-ubuntu*.pkg.tar.xz

RUN aurget freetype2-ubuntu
RUN pacman -Rdd --noconfirm freetype2
RUN pacman -U --noconfirm /aur/freetype2-ubuntu*.pkg.tar.xz

RUN aurget fontconfig-ubuntu
RUN pacman -Rdd --noconfirm fontconfig
RUN pacman -U --noconfirm /aur/fontconfig-ubuntu*.pkg.tar.xz

# RUN aurget ubuntu-themes
# RUN pacman -U --noconfirm /aur/ubuntu-themes*.pkg.tar.xz

RUN rm -rf /aur

RUN wget https://github.com/dockercask/packages/raw/master/ubuntu-themes-14.04.16.04.20160415-1-any.pkg.tar.xz
RUN pacman -Udd --noconfirm /ubuntu-themes-14.04.16.04.20160415-1-any.pkg.tar.xz
RUN rm -f /ubuntu-themes-14.04.16.04.20160415-1-any.pkg.tar.xz

RUN pacman -S --noconfirm xorg-xauth xfce4 xfce4-notifyd lxappearance numix-themes gtk-engines gtk-engine-aurora gtk-engine-murrine human-icon-theme xcursor-vanilla-dmz
