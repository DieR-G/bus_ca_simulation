import numpy as np
import data_loader

coordinates = data_loader.load_coordinates()
network = data_loader.load_network()

### visualization related things
def interpolate_coordinates(start, end, num_points):
    lon_values = np.linspace(start[0], end[0], num_points + 1)
    lat_values = np.linspace(start[1], end[1], num_points + 1)
    return list(zip(lon_values, lat_values))

def create_arc_coordinates():
    arc_coordinates = { 
        (i, j): interpolate_coordinates(coordinates[i], coordinates[j], weight*60)
        for i, connections in enumerate(network)
        for j, weight in connections
    }
    return arc_coordinates
######

def create_arcs():
    arc_positions = {
        (i, j): [False]*weight*60
        for i, arc in enumerate(network)
        for j, weight in arc
    }
    return arc_positions