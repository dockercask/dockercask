FROM dockercask/base-xorg
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN dpkg --add-architecture i386
RUN apt-get update
RUN apt-get install --assume-yes steam

ADD init.sh .
CMD ["sh", "init.sh"]
