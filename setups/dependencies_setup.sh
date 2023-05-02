#/!/bin/bash

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl lsb-release
sudo apt-get install -y libssl-dev libz-dev python3-pip
sudo apt-get install -y vim
sudo apt-get install -y dstat
sudo apt-get install -y lsof
sudo apt-get install -y tcpdump
pip install ipdb