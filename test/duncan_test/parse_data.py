import numpy as np

mesh = open("test_mesh.txt", 'r+')
mesh = mesh.read()
mesh = mesh[6:len(mesh)-2]  # remove 'mesh=c ...' and '... \n from the beginning and end of the string
mesh_list = mesh.split('c')
mesh_array = np.asarray(mesh_list)
mesh_mat = np.reshape(mesh_array, (len(mesh_list) / 3, 3))
mesh_mat = mesh_mat.astype('float64')
print(mesh_mat)