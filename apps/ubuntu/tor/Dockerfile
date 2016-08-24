FROM dockercask/base-xorg
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN sudo apt-key adv --keyserver hkp://keys.gnupg.net --recv-keys A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89
RUN echo "deb http://deb.torproject.org/torproject.org xenial main" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install --assume-yes tor deb.torproject.org-keyring

ADD init.sh .
CMD ["sh", "init.sh"]
