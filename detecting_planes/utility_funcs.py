import numpy as np
import math

def magnitude(vec):
    """
    Returns the magnitude of the input vector
    """
    return math.sqrt(vec[0]**2+vec[1]**2+vec[2]**2)

def cross(vec1, vec2):
    """
    Returns the cross product of vec1 and vec2
    """
    return ((vec1[1]*vec2[2]-vec1[2]*vec2[1]),(vec1[0]*vec2[2]-vec1[2]*vec2[0]),
    (vec1[0]*vec2[1]-vec1[1]*vec2[0]))

def avg_normals(norm1, norm2):
    """
    Returns the average vector of norm1 and norm2
    """
    return ((norm1[0]+norm2[0])/2,(norm1[1]+norm2[1])/2,(norm1[2]+norm2[2])/2)

def find_normal(list1, list2, list3):
    """
    Takes in three points, return the unit normal vector to the plane that they
    lie in.
    """
    vec1 = (list2[0]-list1[0],list2[1]-list1[1],list2[2]-list1[2])
    vec2 = (list3[0]-list1[0],list3[1]-list1[1],list3[2]-list1[2])
    norm = cross(vec1, vec2)
    mag = magnitude(norm)
    for i in range(3):
        unit_normal = (norm[0]/mag,norm[1]/mag,norm[2]/mag)
    return unit_normal

# currently an unused function, but will keep in case I need it later:
# def remove_duplicate_coords(*facets):
#     """
#     Takes any number of facets (sets of 3 coordinates) as inputs and returns a
#     list of coordinates in those facets with no duplicates
#     """
#     return_list = []
#     for i in range(len(facets)):
#         for j in range(3):
#             for k in range(len(return_list)):
#                 if facets[i][j] != return_list[k]:
#                     return_list.append(facets[i][j])
#     return return_list
