import numpy as np
import stl
from stl import mesh
import pickle

from making_test_stl import make_test_cube
import utility_funcs as uf

THRESHOLD = 0.01 # threshold for difference between facet/plane normal uf.crosses

class Stl():
    """
    When make_all() is called, the stl is transformed into a variety of data
    structures, including:
    - a coordinate matrix (len(mesh)x3x3 matrix)
    - a array of facet normals
    - an adjacency populated with the uf.cross of adjacent facets' normals
    """
    def __init__(self, name='', mesh=None):
        if mesh == None: # handling initialization case for mutable obj
            mesh = []
        self.mesh = mesh

    def make_coord_mat(self):
        """
        Restructures the mesh data to a len(mesh)x3x3 matrix
        """
        mesh = self.mesh
        len_mesh = len(mesh)
        coord_mat = np.ndarray((len_mesh,3,3))
        # break up facets into sets of three coordinates
        for j in range(len_mesh):
            coord_mat[j][0] = mesh[j][0:3]
            coord_mat[j][1] = mesh[j][3:6]
            coord_mat[j][2] = mesh[j][6:9]
        self.coord_mat = coord_mat

    def make_normal_arr(self):
        """
        Takes in the coordinate matrix made by make_coord_mat() and returns a
        numpy array of the normals to each respective set of 3 points (structured
        as a tuple with three elements)
        """
        coord_mat = self.coord_mat
        normal_arr = np.ndarray((len(coord_mat),3))
        for i in range(len(coord_mat)):
            facet = coord_mat[i]
            normal_arr[i] = uf.find_normal(facet[0],facet[1],facet[2])
        self.normal_arr = normal_arr

    def make_adjacency_matrix(self):
        """
        Takes a mesh object as an input and creates an adjacency matrix indexed by
        the integer index associated with a facet in the mesh object. The values
        of the adjacency matrix are either None if the facets are not adjacent or
        the uf.magnitude of the uf.cross product of the adjacent facets' normal vectors.
        """
        mesh = self.mesh
        len_mesh = len(mesh)
        coord_mat = self.coord_mat
        normal_arr = self.coord_mat
        adj_mat = np.full((len_mesh,len_mesh),None)
        # create an adjacenty matrix for the mesh object
        for i in range(len_mesh):
            facet_a = coord_mat[i]
            for coord1 in facet_a:
                for j in range(len_mesh):
                    facet_b = coord_mat[j]
                    for coord2 in facet_b:
                        if [coord1[0],coord1[1],coord1[2]] == [coord2[0],coord2[1],coord2[2]]:
                            adj_mat[i][j] = uf.magnitude(uf.cross(uf.find_normal(normal_arr[i][0],normal_arr[i][1],normal_arr[i][2]),
                            uf.find_normal(normal_arr[j][0],normal_arr[j][1],normal_arr[j][2])))
        self.adj_mat = adj_mat

    def make_all(self):
        self.make_coord_mat()
        self.make_normal_arr()
        self.make_adjacency_matrix()

    def __str__(self):
        print('Stl name: \n', self.name)
        print('Mesh: \n', self.mesh)
        print('Coordinate Matrix: \n', self.coord_mat)
        print('Normal Array: \n', self.normal_arr)
        print('Adjacency Matrix: \n', self.adj_mat)
        
class CompositePlanes():
    """
    A composite plane is a plane that represents the plane of best fit for a
    series of facets that are filtered prior to calculating the plane of best
    fit to have normals nearly colinear with the plane's existing normal. Facets
    are numpy arrays and normals are tuples of length 3.
    """
    def __init__(self, adj_mat=None):
        """
        Initialize the plane with two facets; more facets are added into the
        composite plane after the fact.
        """
        self.adj_mat = adj_mat
        # Note: it is intentional that the mutable argument is being handled
        # this way because I want all composite planes objects to have the same
        # adj_mat attribute.

        self.all_facet_index_list = []
        self.all_facet_list = []
        self.plane_list = [] # [((norm),[facets],[facet_indexes]),((norm),[facets],[facet_indexes]),...]

    def check_facet(self, facet, facet_index, plane_index):
        """
        Before a facet is added to the composite plane, it must be filtered to
        see if its normal is colinear enough with self.norm to be considered
        part of the same plane. Returns true if it is, and false if it isn't.
        """
        facet_norm = uf.find_normal(facet[0],facet[1],facet[2])
        plane = self.plane_list[plane_index]
        for i in range(len(plane[1])):
            if uf.magnitude(uf.cross(facet_norm, plane[0])) < THRESHOLD:
                for index in plane[2]:
                    # check for adjacency
                    if self.adj_mat[facet_index][index] != None and index != facet_index:
                        return True
        else:
            return False

    def update_plane_norm(self, plane_index):
        """
        Updates the normal vector based on the average normal vector of the
        facets in self.facets
        """
        norm = (0,0,0)
        plane = self.plane_list[plane_index]
        for facet in plane[1]:
            norm = norm + uf.find_normal(facet[0],facet[1],facet[2])
        self.norm = (norm[0]/len(plane[1]),norm[1]/len(plane[1]),
            norm[2]/len(self.all_facet_index_list))

    def add_facet(self, facet, index):
        """
        Adds a facet to the self.facets if its normal is colinear enough, and
        update's self.norm. Returns true if it was added and false if it wasn't.
        The purpose of returning a true or false is that this metod can be used
        to determine whether the facet is being used in the plane or not; the
        code that uses this method will store the facets that have already been
        added to planes in a dictionary, and the code will need to know whether
        to add the facet or not.
        """
        flag = False
        for i in range(len(self.plane_list)):
            if self.check_facet(facet = facet, facet_index = index, plane_index = i):
                # the facet is not already in the composite plane, is adjacent, to
                # at least one other facet, and has a normal that is nearly colinear
                # with the plane's normal
                self.all_facet_index_list.append(index)
                self.plane_list[i][2].append(index)

                self.plane_list[i][1].append(facet)
                self.all_facet_list.append(facet)
                self.update_plane_norm(plane_index = i)
                flag = True
            else:
                continue

        if flag == False:
            facet_norm = uf.find_normal(facet[0],facet[1],facet[2])
            # create new plane
            self.plane_list.append((facet_norm, [facet], [index]))

            self.all_facet_index_list.append(index)
            self.all_facet_list.append(facet)

    def __str__(self):
        rtn_text = []
        for plane in self.plane_list:
            norm = str(plane[0])
            facets = ''
            for facet in plane[1]:
                facets = facets + str(facet)
            rtn_text.append("Normal: {}\nFacets: {}\n\n".format(norm, facets))
        print_text = ''
        for plane_text in rtn_text:
            print_text = print_text + plane_text
        return "\n{} Planes found:\n\n".format(len(self.plane_list))+print_text
