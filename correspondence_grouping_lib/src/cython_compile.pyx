from libcpp.string cimport string

cdef extern from "correspGroup.h":
    void find (char *string model_filename, char *scene_filename);

def py_hello(name: bytes) -> None:
hello(name)