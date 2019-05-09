rm -rf build;
mkdir build;
cd build;
cmake ..;
make;
mv libCorrespGroup.so ../
cd ..;
pip3 install cython;
python setup.py build_ext --inplace;