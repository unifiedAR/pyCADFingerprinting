from libcpp.string cimport string

cdef extern from "correspGroup.h":
    void find (char *model_filename, char *scene_filename);

def pyCorrespGroup(name: bytes) -> none;
    find(name)