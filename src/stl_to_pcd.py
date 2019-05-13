import pcl
import numpy as np
from stl import mesh

mesh = mesh.Mesh.from_file('mesh_folder/model.stl')
mesh = mesh.astype('float32')

pcl.save(pc, 'mesh_folder/mesh.pcd', format='pcd')