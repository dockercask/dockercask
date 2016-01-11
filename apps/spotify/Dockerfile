FROM dockercask/base-xorg
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

# RUN aurget libcurl-compat
# RUN pacman -U --noconfirm /aur/libcurl-compat*.pkg.tar.xz

# RUN aurget spotify
# RUN pacman -U --noconfirm /aur/spotify*.pkg.tar.xz

# RUN rm -rf /aur

RUN wget https://github.com/dockercask/packages/raw/master/libcurl-compat-7.46.0-2-x86_64.pkg.tar.xz
RUN pacman -U --noconfirm /libcurl-compat-7.46.0-2-x86_64.pkg.tar.xz
RUN rm -f /libcurl-compat-7.46.0-2-x86_64.pkg.tar.xz

RUN wget https://github.com/dockercask/packages/raw/master/spotify-1.0.19.106-3-x86_64.pkg.tar.xz
RUN pacman -U --noconfirm /spotify-1.0.19.106-3-x86_64.pkg.tar.xz
RUN rm -f /spotify-1.0.19.106-3-x86_64.pkg.tar.xz

ADD init.sh .
CMD ["sh", "init.sh"]
