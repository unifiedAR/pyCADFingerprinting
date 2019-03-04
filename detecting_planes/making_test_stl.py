import numpy as np
import stl
from stl import mesh

def make_test_cube():
    data = np.zeros(7, dtype=mesh.Mesh.dtype)

    data['vectors'][0] = np.array([[0,1,1],[1,0,1],[0,0,1]])
    data['vectors'][1] = np.array([[1,0,1],[0,1,1],[1,1,1]])
    data['vectors'][2] = np.array([[1,0,0],[1,0,1],[1,1,0]])
    data['vectors'][3] = np.array([[1,1,1],[1,0,1],[1,1,0]])
    data['vectors'][4] = np.array([[0,0,0],[1,0,0],[1,0,1]])
    data['vectors'][5] = np.array([[0,0,0],[0,0,1],[1,0,1]])
    data['vectors'][6] = np.array([[0,0,1],[0,1,1],[0,1,0]])
    cube = stl.base.BaseMesh(data,remove_empty_areas = False)
    cube.update_normals()

    return cube
