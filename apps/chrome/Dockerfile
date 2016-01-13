FROM dockercask/base-xorg
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN pacman -S --noconfirm ffmpeg gst-plugins-good gst-plugins-ugly

# RUN aurget google-chrome
# RUN pacman -U --noconfirm /aur/google-chrome*.pkg.tar.xz
# RUN rm -rf /aur

RUN wget https://github.com/dockercask/packages/raw/master/google-chrome-47.0.2526.106-1-x86_64.pkg.tar.xz
RUN pacman -U --noconfirm /google-chrome-47.0.2526.106-1-x86_64.pkg.tar.xz
RUN rm -f /google-chrome-47.0.2526.106-1-x86_64.pkg.tar.xz

ADD init.sh .
CMD ["sh", "init.sh"]
