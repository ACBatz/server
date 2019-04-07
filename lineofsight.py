import math
import numpy as np

def distance(p_1, p_2):
    return math.sqrt(math.pow(p_1[0] - p_2[0], 2) + math.pow(p_1[1] - p_2[1], 2) + math.pow(p_1[2] - p_2[2], 2))

def los(p1, p2):
    x0 = p1[0]
    y0 = p1[1]
    z0 = p1[2]
    x1 = p2[0]
    y1 = p2[1]
    z1 = p2[2]
    e_r = 6378137 / 1000
    midp = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    dist = distance((0,0,0), midp)
    if dist > e_r:
        return True
    else:
        return False

# def angle(p1, p2):
#     x0 = p1[0]
#     y0 = p1[1]
#     z0 = p1[2]
#     x1 = p2[0]
#     y1 = p2[1]
#     z1 = p2[2]
#     xc = 0
#     yc = 0
#     zc = 0
#     v_p1_c = ((xc - x0), (yc - y0), (zc - z0))
#     v_p1_p2 = ((x1 - x0), (y1 - y0), (z1 - z0))
#     v_p1_c_mag = math.sqrt(math.pow(v_p1_c[0],2) + math.pow(v_p1_c[1],2) + math.pow(v_p1_c[2],2))
#     v_p1_c_norm = (v_p1_c[0] / v_p1_c_mag, v_p1_c[1] / v_p1_c_mag, v_p1_c[2] / v_p1_c_mag)
#     v_p1_p2_mag = math.sqrt(math.pow(v_p1_p2[0],2) + math.pow(v_p1_p2[1],2) + math.pow(v_p1_p2[2],2))
#     v_p1_p2_norm = (v_p1_p2[0] / v_p1_p2_mag, v_p1_p2[1] / v_p1_p2_mag, v_p1_p2[2] / v_p1_p2_mag)
#     res = v_p1_c_norm[0] * v_p1_p2_norm[0] + v_p1_c_norm[1] * v_p1_p2_norm[1] + v_p1_c_norm[2] * v_p1_p2_norm[2]
#     return math.acos(res)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)) * 180 / math.pi

def ground_los(station, sat):
    v1 = ((sat[0] - station[0] / 1000), (sat[1] - station[1] / 1000), (sat[2] - station[2] / 1000))
    v2 = ((0 - station[0] / 1000), (0 - station[1] / 1000), (0 - station[2] / 1000))
    dist = distance((station[0] / 1000, station[1] / 1000, station[2] / 1000), sat)
    return True if angle_between(v1, v2) > 90 else False