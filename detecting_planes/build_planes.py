import stl
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits import mplot3d

from making_test_stl import make_test_cube, make_any_stl
import utility_funcs as uf
from classes import Stl
from classes import CompositePlanes

THRESHOLD = 0.01 # threshold for difference between facet/plane normal uf.crosses

cube = make_test_cube() # test stl

dict_of_facets = {}
dict_of_comp_planes = {}

################################################################## Visualize STL

def plot_stl(item):
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(item.vectors))
    scale = item.points.flatten(-1)
    axes.auto_scale_xyz(scale,scale,scale)
    pyplot.show()

################################################# Algorithm for detecting planes

if __name__=="__main__":
    #stl = Stl('cube', cube)
    stl_object = Stl('our_file', make_any_stl("original2.stl"))

    plot = input("\nDisplay the stl? y/n ----> ")
    if plot == 'y' or plot == 'Y':
        print("Plotting stl; close the window to calculate the planes.")
        plot_stl(stl_object.mesh)
    elif plot == 'n' or plot == "N":
        print("Okay, won't plot the graph.\n")
    else:
        print("Invalid response; will not plot the stl. \n")

    stl_object.make_all() # generate all object attributes
    comp_planes = CompositePlanes(stl_object.adj_mat)

    print("Calculating planes in stl...")

    for i in range(len(stl_object.coord_mat)):
        comp_planes.add_facet(stl_object.coord_mat[i], i)

    print("Planes calculated!")
    print(comp_planes)
