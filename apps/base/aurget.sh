#!/bin/bash
useradd pacman
echo "pacman ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
cd /tmp
sudo -u pacman wget https://aur4.archlinux.org/cgit/aur.git/snapshot/$1.tar.gz
sudo -u pacman tar xfz $1.tar.gz
rm $1.tar.gz
cd $1
sudo -u pacman makepkg --syncdeps --noconfirm
mkdir -p /aur
cp $1*.pkg.tar.xz /aur
cd ..
rm -rf $1
userdel pacman
sed -i '/pacman ALL=(ALL) NOPASSWD: ALL/d' /etc/sudoers
