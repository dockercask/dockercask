FROM dockercask/base-xorg
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN pacman -S --noconfirm firefox ffmpeg gst-plugins-good gst-plugins-ugly

# RUN aurget chromium-pepper-flash
# RUN pacman -U --noconfirm /aur/chromium-pepper-flash*.pkg.tar.xz

# RUN aurget freshplayerplugin
# RUN pacman -U --noconfirm /aur/freshplayerplugin*.pkg.tar.xz

# RUN rm -rf /aur

RUN wget https://github.com/dockercask/packages/raw/master/chromium-pepper-flash-1:20.0.0.228-1-x86_64.pkg.tar.xz
RUN pacman -U --noconfirm /chromium-pepper-flash-1:20.0.0.228-1-x86_64.pkg.tar.xz
RUN rm -f /chromium-pepper-flash-1:20.0.0.228-1-x86_64.pkg.tar.xz

RUN wget https://github.com/dockercask/packages/raw/master/freshplayerplugin-0.3.4-1-x86_64.pkg.tar.xz
RUN pacman -U --noconfirm /freshplayerplugin-0.3.4-1-x86_64.pkg.tar.xz
RUN rm -f /freshplayerplugin-0.3.4-1-x86_64.pkg.tar.xz

RUN sudo -u docker echo "enable_3d = 0" > /home/docker/.config/freshwrapper.conf

ADD init.sh .
CMD ["sh", "init.sh"]
