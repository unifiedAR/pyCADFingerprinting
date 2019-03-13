import numpy as np
import stl
from stl import mesh
import pickle

from making_test_stl import make_test_cube
import utility_funcs as uf

THRESHOLD = 0.5  # threshold for difference between facet/plane normal uf.crosses


class Stl():
    """
    When make_all() is called, the stl is transformed into a variety of data
    structures, including:
    - a coordinate matrix (len(mesh)x3x3 matrix)
    - a array of facet normals
    - an adjacency populated with the uf.cross of adjacent facets' normals
    """

    def __init__(self, name='', mesh=None):
        if mesh == None:  # handling initialization case for mutable obj
            mesh = []
        self.mesh = mesh

    def make_coord_mat(self):
        """
        Restructures the mesh data to a len(mesh)x3x3 matrix
        """
        mesh = self.mesh
        len_mesh = len(mesh)
        coord_mat = np.ndarray((len_mesh, 3, 3))
        # break up facets into sets of three coordinates
        if len(mesh) > 200:
            modulus_num = 1
        else:
            modulus_num = int(len(mesh) / 200)
        for j in range(len_mesh):
            if j % modulus_num == 0:
                coord_mat[j][0] = mesh[j][0:3]
                coord_mat[j][1] = mesh[j][3:6]
                coord_mat[j][2] = mesh[j][6:9]
        self.coord_mat = coord_mat
        self.num_triangles = len(coord_mat)
        print(self.num_triangles)

    def make_normal_arr(self):
        """
        Takes in the coordinate matrix made by make_coord_mat() and returns a
        numpy array of the normals to each respective set of 3 points (structured
        as a tuple with three elements)
        """
        coord_mat = self.coord_mat
        normal_arr = np.ndarray((len(coord_mat), 3))
        for i in range(len(coord_mat)):
            facet = coord_mat[i]
            normal_arr[i] = uf.find_normal(facet[0], facet[1], facet[2])
        self.normal_arr = normal_arr

    def make_adjacency_matrix(self):
        """
        Takes a mesh object as an input and creates an adjacency matrix indexed by
        the integer index associated with a facet in the mesh object. The values
        of the adjacency matrix are either None if the facets are not adjacent or
        the uf.magnitude of the uf.cross product of the adjacent facets' normal vectors.
        """
        normal_arr = self.coord_mat
        adj_mat = np.full((len_mesh, len_mesh), None)
        # create an adjacenty matrix for the mesh object
        n = 0
        for i in range(self.num_triangles):
            facet_a = self.coord_mat[i]
            for coord1 in facet_a:
                for j in range(self.num_triangles):
                    facet_b = self.coord_mat[j]
                    for coord2 in facet_b:
                        if [coord1[0], coord1[1], coord1[2]] == [coord2[0], coord2[1], coord2[2]]:
                            adj_mat[i][j] = uf.magnitude(
                                uf.cross(uf.find_normal(normal_arr[i][0], normal_arr[i][1], normal_arr[i][2]),
                                         uf.find_normal(normal_arr[j][0], normal_arr[j][1], normal_arr[j][2])))
        self.adj_mat = adj_mat

    def make_all(self):
        self.make_coord_mat()
        self.make_normal_arr()
        # self.make_adjacency_matrix()

    def __str__(self):
        print('Stl name: \n', self.name)
        print('Mesh: \n', self.mesh)
        print('Coordinate Matrix: \n', self.coord_mat)
        print('Normal Array: \n', self.normal_arr)
        print('Adjacency Matrix: \n', self.adj_mat)


class NewCompositePlanes():
    def __init__(self, stl_object):
        self.stl_object = stl_object
        self.normals_used = []
        self.pl = np.ndarray((1), dtype=np.ndarray)

    def build_planes(self):
        """
        pl[i][j][k] contains a list of composite planes with that normal, where
        each composite plane is a list of adjacent facets that share that
        normal.
        """
        pl = np.ndarray((11, 11, 11), dtype=np.ndarray)
        for i in range(self.stl_object.num_triangles):
            print("Progress:", round(100*i/self.stl_object.num_triangles), "%", end="\r")
            facet = self.stl_object.coord_mat[i]
            facet_norm = self.stl_object.normal_arr[i]
            rfn = (
                int(10 * round(facet_norm[0], 1)), int(10 * round(facet_norm[1], 1)), int(10 * round(facet_norm[2], 1)))
            if pl[rfn[0]][rfn[1]][rfn[2]] is not None:
                # Check whether te facet is adjacent to any other facets in
                # the composite plane by seeing if there are any mutual
                # points between them:
                flag = False
                for j in range(len(pl[rfn[0]][rfn[1]][rfn[2]])):
                    comp_plane = [pl[rfn[0]][rfn[1]][rfn[2]][j]]
                    for comp_facet in comp_plane:
                        for facet_coord in facet:
                            if facet_coord in comp_facet:
                                comp_pl_index = j
                                flag = True

                if flag:
                    # If the code has reached here, then there are mutual pts between the facet and the composite plane
                    # at index j
                    c = np.ndarray((1), dtype=np.ndarray)
                    c[0] = facet
                    print(pl[rfn[0]][rfn[1]][rfn[2]][comp_pl_index], '\n\n', c)
                    pl[rfn[0]][rfn[1]][rfn[2]][comp_pl_index] = np.concatenate((pl[rfn[0]][rfn[1]][rfn[2]][comp_pl_index], c))
                else:
                    # If the code has reached here, then there are no composite planes that the facet can be added to,
                    # so a new composite plane will be added and initialized with that facet

                    # Add and initialize a new comp plane
                    pl[rfn[0]][rfn[1]][rfn[2]] = np.concatenate((pl[rfn[0]][rfn[1]][rfn[2]], np.ndarray((1), dtype=np.ndarray)))
                    pl[rfn[0]][rfn[1]][rfn[2]][-1] = np.ndarray((1), dtype=np.ndarray)

                    # Add a new facet to the comp plane
                    # pl[rfn[0]][rfn[1]][rfn[2]][-1] = np.concatenate((pl[rfn[0]][rfn[1]][rfn[2]][-1], np.ndarray((1), dtype=np.ndarray)))
                    pl[rfn[0]][rfn[1]][rfn[2]][-1][0] = facet

            else:
                print("Other")
                # No facets have matched this normal yet
                pl[rfn[0]][rfn[1]][rfn[2]] = np.ndarray((1), dtype=np.ndarray)  # hold the list of composite planes
                pl[rfn[0]][rfn[1]][rfn[2]][0] = np.ndarray((1), dtype=np.ndarray)  # an array to hold the facets
                pl[rfn[0]][rfn[1]][rfn[2]][0][0] = facet
                self.normals_used.append((rfn[0] / 10, rfn[1] / 10, rfn[2] / 10))
        self.pl = pl

    def __str__(self):
        print("All normals: \n", self.pl)
        print("Normals used: \n", len(self.normals_used))
