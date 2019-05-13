import numpy as np
import pcl
import os


def text_to_pcd(mesh):
    """
    Converts text in the form of a csv (delimiter='c') that represents a 3D point cloud into a pcl.PointCLoud
    :param mesh: text in the form of a csv (delimiter='c') from a Unity mesh
    :return: PointCloud object
    """
    mesh = mesh[6:len(mesh) - 2]  # remove 'mesh=c ...' and '... \n from the beginning and end of the string
    mesh_list = mesh.split('c')
    mesh_array = np.asarray(mesh_list)
    mesh_mat = np.reshape(mesh_array, (int(len(mesh_list) / 3), 3))
    mesh_mat = mesh_mat.astype('float32')
    return pcl.PointCloud(mesh_mat)


def save_text_to_pcd(mesh, path='auto', file_name='scene_mesh.pcd'):
    """
    Saves a text of a mesh from Unity to a .pcd file to be used for correspondence grouping
    :param mesh: text in the form of a csv (delimiter='c') from a Unity mesh
    :param path: directory to save the pcd
    :param file_name: name of the pcd file
    :return: void
    """
    if path == 'auto':
        cwd = os.getcwd()
        len_cwd = len(cwd)
        if cwd[len_cwd - 20:len_cwd] == '/pyCADFingerprinting':
            print('In the /pyCADFingerprinting directory')
            cwd = os.path.join(cwd, 'src')
        elif cwd[len_cwd - 4:len_cwd] == '/src':
            print('In the /pyCADFingerprinting/src directory')
        file_path = os.path.join(cwd, 'mesh_folder', file_name)
    else:
        file_path = os.path.join(path, file_name)
    pc = text_to_pcd(mesh)
    pcl.save(pc, file_path, format='pcd', binary=True)


if __name__ == '__main__':
    mesh = open('test_mesh.txt', 'r+')
    mesh = mesh.read()
    pc = save_text_to_pcd(mesh)
