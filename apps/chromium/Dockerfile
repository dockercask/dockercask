FROM dockercask/base-xorg
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN pacman -S --noconfirm chromium ffmpeg gst-plugins-good gst-plugins-ugly

ADD init.sh .
CMD ["sh", "init.sh"]
