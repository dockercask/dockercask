### archlinux install

```bash
pacman -S xsel xorg-server-xephyr docker util-linux xorg-xauth
systemctl start docker.service
```

### ubuntu install

```bash
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo sh -c 'echo "deb https://apt.dockerproject.org/repo ubuntu-`lsb_release -c -s` main" > /etc/apt/sources.list.d/docker.list'
sudo apt-get update
sudo apt-get install xsel xserver-xephyr docker-engine linux-image-extra-virtual
sudo service docker start
```

### init

```bash
python2 dockercask.py build base
python2 dockercask.py add firefox
python2 dockercask.py add spotify
python2 dockercask.py build firefox
python2 dockercask.py build spotify
```

### run app

```bash
python2 dockercask.py run firefox
```
