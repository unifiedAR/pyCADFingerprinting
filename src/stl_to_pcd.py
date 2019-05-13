import pcl
import numpy as np
from stl import mesh

mesh = mesh.Mesh.from_file('mesh_folder/model.stl')
npmesh = mesh.points.reshape(len(mesh.points)*3, 3)
npmesh = np.unique(npmesh, axis=0)
npmesh = npmesh.astype('float32')
pc = pcl.PointCloud(npmesh)
pcl.save(pc, 'mesh_folder/mesh.pcd', format='pcd', binary=True)
