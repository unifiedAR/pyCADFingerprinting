#!/usr/bin/env bash
cd /home/
apt-get update;
apt-get install curl;
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py;
pip install virtualenv;
mkdir python-virtual-environments && cd python-virtual-environments
apt-get install python3-venv
python3 -m venv env;
source env/bin/activate;
cd /home/pyCADFingerprinting/correspondence_grouping_lib;
mkdir build;
cd build;
cmake ..;
make -j8;
mv libCorrespGroup.so ../src/
cd ../src/;
pip3 install cython;

python setup.py build_ext --inplace;