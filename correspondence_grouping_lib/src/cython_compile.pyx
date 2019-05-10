# cdef extern from "correspGroup.h":
#     void CorrespGroup :: find (char *model_filename, char *scene_filename);

cdef extern from "correspGroup.h":
    void find (char *model_filename, char *scene_filename);

def pyCorrespGroup(model_filename: bytes, scene_filename: bytes) -> None:
    find(model_filename, scene_filename)
