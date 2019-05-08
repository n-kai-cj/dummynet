#!/bin/bash

sudo apt update
sudo apt install make git gcc build-essential bc bison libtool automake autoconf flex libncurses5-dev -y


sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source && sudo chmod +x /usr/bin/rpi-source && /usr/bin/rpi-source -q --tag-update

sudo mkdir -p /usr/src/rpi-header-`uname -r`

sudo rpi-source -d /usr/src/rpi-header-`uname -r`

sudo chmod 777 -R /usr/src/rpi-header-`uname -r`

