from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

examples_extension = Extension(
    name="corresp_group_python",
    sources=["cython_compile.pyx"],
    libraries=["libCorrespGroup"],
)
setup(
    name="corresp_group_python",
    ext_modules=cythonize([examples_extension])
)