import numpy as np  
import pcl
import os

def load_mesh(mesh_filename='test_mesh.txt'):
    mesh = open(mesh_filename, 'r+')
    mesh = mesh.read()
    mesh = mesh[6:len(mesh)-2]  # remove 'mesh=c ...' and '... \n from the beginning and end of the string
    mesh_list = mesh.split('c')
    mesh_array = np.asarray(mesh_list)
    mesh_mat = np.reshape(mesh_array, (int(len(mesh_list) / 3), 3))
    mesh_mat = mesh_mat.astype('float32')
    print(mesh_mat)
    pc = pcl.PointCloud(mesh_mat)
    return pc

if __name__ == '__main__':
    pc = load_mesh()
    path = os.getcwd() + "/pcd_test.pcd"
    pcd.save(pc, path, format="pcd")