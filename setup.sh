#!/usr/bin/env bash
cd /home/
apt-get update;
apt-get install curl;
apt-get install python3-dev;
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py;
pip install --upgrade pip;
pip install virtualenv;
pip install numpy;
pip install flask;
pip install flask_session;
pip install cython;
mkdir python-virtual-environments && cd python-virtual-environments
apt-get install python3-venv
python3 -m venv env && source env/bin/activate;
cd /home/
git clone https://github.com/strawlab/python-pcl.git;
cd python-pcl/;
pip install .;
cd /home/pyCADFingerprinting/;
mkdir build;
cd build;
cmake ..;
make -j8;
mv libCorrespGroup.so ../src/correspGroup
cd /home/pyCADFingerprinting/