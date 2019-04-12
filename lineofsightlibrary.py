import numpy as np
import sys

from satellite import Satellite
from station import Station
from vectorlibrary import angle_between, normalize_vector, get_angle_remaining
from routetree import RouteTree

center = np.array([0, 0, 0])

def distance_between_points(p0, p1):
    return np.linalg.norm(p0 - p1)

def satellites_have_line_of_sight(s0, s1):
    x0, y0, z0 = s0
    x1, y1, z1 = s1

    earth_radius = 6378137 / 1000

    midpoint = np.array([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return True if distance_between_points(center, midpoint) > earth_radius else False

def station_has_line_of_sight(station_position, satellite_position):
    x0, y0, z0 = station_position
    x1, y1, z1 = satellite_position

    p0 = np.array([x0, y0, z0])
    p1 = np.array([x1 * 1000, y1 * 1000, z1 * 1000])

    v_p0_c = center - p0
    v_p0_p1 = p1 - p0

    v_p0_c_hat = normalize_vector(v_p0_c)
    v_p0_p1_hat = normalize_vector(v_p0_p1)

    return True if angle_between(v_p0_c_hat, v_p0_p1_hat) > 90 else False

def angle_between_stations(s0, s1):
    x0, y0, z0 = s0
    x1, y1, z1 = s1

    p0 = np.array([x0, y0, z0])
    p1 = np.array([x1, y1, z1])

    v_c_p0 = p0 - center
    v_c_p1 = p1 - center

    v_c_p0_hat = normalize_vector(v_c_p0)
    v_c_p1_hat = normalize_vector(v_c_p1)

    return angle_between(v_c_p0_hat, v_c_p1_hat)

def get_best_path(station1, station2, satellites, time):
    stat_pos1 = station1.get_ecef_position()
    stat_pos2 = station2.get_ecef_position()

    stat1_los = list(filter(lambda x: station_has_line_of_sight(stat_pos1, x.get_propagation(time)[0]), satellites))
    if len(stat1_los) == 0:
        raise Exception('No satellites are in the line of sight with origin station [{}]'.format(station1.id))
    else:
        min_angle = 360
        min_angle_satellite = None
        for sat in stat1_los:
            angle = get_angle_remaining(stat_pos1, stat_pos2, sat.get_propagation(time)[0])
            if angle < min_angle:
                min_angle = angle
                min_angle_satellite = sat
        route = [station1, min_angle_satellite]
        get_next_route_recursive(stat_pos1, stat_pos2, min_angle_satellite, satellites, time, route)
        route.append(station2)
        return route

def get_next_route_recursive(stat_pos1, stat_pos2, satellite, satellites, time, route):
    if station_has_line_of_sight(stat_pos2, satellite.get_propagation(time)[0]):
        route.append(satellite)
        return route
    else:
        sats_los = list(filter(lambda x: satellites_have_line_of_sight(satellite.get_propagation(time)[0], x.get_propagation(time)[0]), satellites))
        if len(sats_los) == 0:
            raise Exception('No satellites are in the line of sight with satellite with id [{}]'.format(satellite.id))
        else:
            min_angle = 360
            min_angle_satellite = None
            for sat in sats_los:
                angle = get_angle_remaining(stat_pos1, stat_pos2, sat.get_propagation(time)[0])
                if angle < min_angle:
                    min_angle = angle
                    min_angle_satellite = sat
            route.append(min_angle_satellite)
            return get_next_route_recursive(stat_pos1, stat_pos2, min_angle_satellite, satellites, time, route)

def do_routing(origin, destination, satellites, time):
    root = RouteTree(time, origin, distance_between_points)
    do_routing_recursive(origin, destination, satellites, time, root)
    return root

def do_routing_recursive(current, destination, satellites, time, routeTree):
        if current == destination:
            return
        elif isinstance(current, Satellite) and station_has_line_of_sight(destination.get_ecef_position(), current.get_propagation(time)[0]):
            routeTree.insert(current, destination, destination)
            do_routing_recursive(destination, destination, satellites, time, routeTree)
        else:
            destination_position = destination.get_ecef_position()
            if isinstance(current, Station):
                x0, y0, z0 = current.get_ecef_position()
            else:
                x0, y0, z0 = current.get_propagation(time)[0]
                x0 = 1000 * x0
                y0 = 1000 * y0
                z0 = 1000 * z0
            origin_position = np.array([x0, y0, z0])
            if isinstance(current, Station):
                sats_in_los = list(filter(lambda x: station_has_line_of_sight(current.get_ecef_position(), x.get_propagation(time)[0]), satellites))
            else:
                sats_in_los = list(
                    filter(lambda x: station_has_line_of_sight(current.get_propagation(time)[0], x.get_propagation(time)[0]),
                           satellites))
            min_angle = 360
            min_angle_satellite = None
            min_distance = sys.maxsize
            min_distance_satellite = None
            sats_have_los_to_destination = []
            for sat in sats_in_los:
                sat_position = sat.get_propagation(time)[0]
                if station_has_line_of_sight(destination_position, sat_position):
                    sats_have_los_to_destination.append(sat)
                else:
                    angle = get_angle_remaining(origin_position, destination_position, sat_position)
                    x0, y0, z0 = destination_position
                    x1, y1, z1 = sat.get_propagation(time)[0]
                    distance = distance_between_points(np.array([x0, y0, z0]), np.array([x1, y1, z1]))
                    if angle < min_angle:
                        min_angle = angle
                        min_angle_satellite = sat
                    if distance < min_distance:
                        min_distance = distance
                        min_distance_satellite = sat
            if len(sats_have_los_to_destination) > 0:
                min_distance = sys.maxsize
                min_distance_satellite = None
                for sat in sats_have_los_to_destination:
                    x0, y0, z0 = destination_position
                    x1, y1, z1 = sat.get_propagation(time)[0]
                    distance = distance_between_points(np.array([x0, y0, z0]), np.array([x1, y1, z1]))
                    if distance < min_distance:
                        min_distance = distance
                        min_distance_satellite = sat
                routeTree.insert(current, min_distance_satellite, min_distance_satellite)
                do_routing_recursive(min_distance_satellite, destination, satellites, time, routeTree)
            else:
                routeTree.insert(current, min_angle_satellite, min_distance_satellite)
                do_routing_recursive(min_angle_satellite, destination, satellites, time, routeTree)
                do_routing_recursive(min_distance_satellite, destination, satellites, time, routeTree)

