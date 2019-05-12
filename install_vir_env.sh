#!/usr/bin/env bash
cd /home/;
apt-get update;
apt-get install curl;
apt-get install python3-dev;
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py;
pip install --upgrade pip;
pip install virtualenv;
mkdir python-virtual-environments;
cd python-virtual-environments/;
apt-get install python3-venv;
python3 -m venv env;
