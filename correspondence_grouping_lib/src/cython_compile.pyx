from libcpp.string cimport string

cdef extern from "correspGroup.h":
    void find (std::string model_filename_, std::string scene_filename_);

def py_hello(name: bytes) -> None:
hello(name)