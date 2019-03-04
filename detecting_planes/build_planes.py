import stl
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits import mplot3d

from making_test_stl import make_test_cube
import utility_funcs as uf
from classes import Stl
from classes import CompositePlanes

THRESHOLD = 0.01 # threshold for difference between facet/plane normal uf.crosses

cube = make_test_cube() # test stl

dict_of_facets = {}
dict_of_comp_planes = {}

################################################################## Visualize STL

def plot_stl():
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube.vectors))
    scale = cube.points.flatten(-1)
    axes.auto_scale_xyz(scale,scale,scale)
    pyplot.show()

################################################# Algorithm for detecting planes

if __name__=="__main__":
    stl = Stl('cube', cube)
    stl.make_all() # generate all object attributes

    plot = input("\nDisplay the stl? y/n ----> ")
    if plot == 'y' or plot == 'Y':
        print("Plotting stl; close the window to calculate the planes.")
        plot_stl()
    elif plot == 'n' or plot == "N":
        print("Okay, won't plot the graph.\n")
    else:
        print("Invalid response; will not plot the stl. \n")

    comp_planes = CompositePlanes(stl.adj_mat)

    print("Calculating planes in stl...")

    for i in range(len(stl.coord_mat)):
        comp_planes.add_facet(stl.coord_mat[i], i)

    print("Planes calculated!")
    print(comp_planes)
