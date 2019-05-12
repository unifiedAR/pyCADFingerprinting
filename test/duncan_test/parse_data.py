import numpy as np
import pcl

mesh = open("test_mesh.txt", 'r+')
mesh = mesh.read()
mesh = mesh[6:len(mesh)-2]  # remove 'mesh=c ...' and '... \n from the beginning and end of the string
mesh_list = mesh.split('c')
mesh_array = np.asarray(mesh_list)
mesh_mat = np.reshape(mesh_array, (len(mesh_list) / 3, 3))
mesh_mat = mesh_mat.astype('float64')
pc = pcl.PointCloud(mesh_mat, dtype=np.float32)


print('Loading point clouds...\n')
object = pc
scene = pc

print('Downsampling...\n')
grid_obj = object.make_voxel_grid_filter()
leaf = 0.005
grid_obj.set_leaf_size (leaf, leaf, leaf)
object = grid_obj.filter()
scene_obj = scene.make_voxel_grid_filter()
grid_sce = scene_obj.filter ()


print('Estimating scene normals...\n')
nest = scene.make_NormalEstimationOMP()
nest.set_RadiusSearch (0.01);
scene = nest.compute ()

print('Estimating features...\n')
fest_obj = object.make_FeatureEstimation()
fest_obj.setRadiusSearch (0.025)
object_features = fest_obj.compute ()

fest_sce = scene.make_FeatureEstimation()
fest_sce.setRadiusSearch (0.025)
scene_features = fest_sce.compute ()


print('Starting alignment...\n')
align = object.make_SampleConsensusPrerejective()
align.setSourceFeatures (object_features)
align.setTargetFeatures (scene_features)
# Number of RANSAC iterations
align.set_MaximumIterations (50000)
# Number of points to sample for generating/prerejecting a pose
align.set_NumberOfSamples (3)
# Number of nearest features to use
align.set_CorrespondenceRandomness (5)
# Polygonal edge length similarity threshold
align.set_SimilarityThreshold (0.9)
# Inlier threshold
align.set_MaxCorrespondenceDistance (2.5 * leaf)


if align.hasConverged () == True:
    # Print results
    print ('\n');
    # Eigen::Matrix4f transformation = align.getFinalTransformation ()
    transformation = align.getFinalTransformation ()
    print(transformation)

    # print ('    | %6.3f %6.3f %6.3f | \n', transformation [0, 0], transformation [0, 1], transformation [0, 2])
    # print ('R = | %6.3f %6.3f %6.3f | \n', transformation [1, 0], transformation [1, 1], transformation [1, 2])
    # print ('    | %6.3f %6.3f %6.3f | \n', transformation [2, 0], transformation [2, 1], transformation [2, 2])
    # print ('\n');
    # print ('t = < %0.3f, %0.3f, %0.3f >\n', transformation[0, 3], transformation[1, 3], transformation[2, 3])
    # print ('\n');
    # print ('Inliers: %i/%i\n', align.getInliers ().size (), object->size ());

    # # Show alignment
    # visu = pcl.PCLVisualization('Alignment')
    # visu.add_PointCloud (scene, ColorHandlerT (scene, 0.0, 255.0, 0.0), 'scene')
    # visu.add_PointCloud (object_aligned, ColorHandlerT (object_aligned, 0.0, 0.0, 255.0), 'object_aligned')
    # visu.spin ()
else:
    print('Alignment failed!\n')
