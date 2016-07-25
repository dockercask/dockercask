FROM dockercask/base-xorg
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN echo -e "[multilib]\nInclude = /etc/pacman.d/mirrorlist" >> /etc/pacman.conf

RUN pacman -Sy
RUN pacman -S --noconfirm lib32-nvidia-libgl
RUN pacman -S --noconfirm steam

ADD init.sh .
CMD ["sh", "init.sh"]
