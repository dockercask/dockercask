FROM dockercask/ubuntu-base
MAINTAINER Zachary Huff <zach.huff.386@gmail.com>

RUN add-apt-repository --yes ppa:graphics-drivers/ppa
RUN apt-get update
RUN apt-get install --assume-yes nvidia-370 nvidia-settings nvidia-libopencl1-370 nvidia-opencl-icd-370

RUN apt-get install --assume-yes libcairo2 libfreetype6 fontconfig
RUN apt-get install --assume-yes light-themes human-icon-theme gnome-human-icon-theme

RUN apt-get install --assume-yes xauth xfwm4 xfce4-panel xfce4-session xfce4-notifyd xfce4-notifyd xfce4-settings lxappearance gtk2-engines gtk2-engines-aurora gtk2-engines-murrine gtk3-engines-xfce xcursor-themes
