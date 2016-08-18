FROM dockercask/base-xorg
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN pacman -S --noconfirm steam

ADD init.sh .
CMD ["sh", "init.sh"]
