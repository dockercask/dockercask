#!/bin/bash
set -e
useradd -m pacman | true
sed -i '/pacman ALL=(ALL) NOPASSWD: ALL/d' /etc/sudoers
echo "pacman ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
rm -rf /tmp/pkg
sudo -u pacman mkdir -p /tmp/pkg
sudo -u pacman cp -r ./* /tmp/pkg
cd /tmp/pkg
sudo -u pacman PKGEXT=.pkg.tar makepkg --syncdeps --noconfirm
mkdir -p /aur
cp *.pkg.tar /aur
cd ..
rm -rf /tmp/pkg
userdel -r pacman
sed -i '/pacman ALL=(ALL) NOPASSWD: ALL/d' /etc/sudoers
