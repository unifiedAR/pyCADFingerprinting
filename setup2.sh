#!/usr/bin/env bash
pip install --upgrade pip;
pip install numpy;
pip install flask;
pip install flask_session;
pip install cython;
pip install scipy;
pip install numpy-stl;
cd /home/
git clone https://github.com/strawlab/python-pcl.git;
cd python-pcl/;
pip install .;
cd /home/pyCADFingerprinting/;
mkdir build;
cd build;
cmake ..;
make -j8;
mv CorrespondenceGrouping ../src/