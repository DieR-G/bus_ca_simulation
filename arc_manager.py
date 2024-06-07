import numpy as np
import json

with open('data/coordinates.json', 'r') as file:
    coordinates = json.load(file)

with open('data/network.json', 'r') as file:
    network = json.load(file)

# Utility functions
def interpolate_coordinates(start, end, num_points):
    lon_values = np.linspace(start[0], end[0], num_points + 1)
    lat_values = np.linspace(start[1], end[1], num_points + 1)
    return list(zip(lon_values, lat_values))


def initialize_arc_coordinates():
    return {
        (i, j): interpolate_coordinates(coordinates[i], coordinates[j], weight * 60)
        for i, connections in enumerate(network)
        for j, weight in connections
    }

def initialize_arc_positions():
    return {
        (i, j): [False] * weight * 60
        for i, arc in enumerate(network)
        for j, weight in arc
    }

def get_arc(bus):
    return bus.get_arc()

def get_arc_position(bus):
    return bus.get_arc_position()

def update_arc_position(bus, position):
    arc = get_arc(bus)
    arc_positions[arc][position] = True

def clear_arc_position( bus, position):
    arc = self.get_arc(bus)
    self.arc_positions[arc][position] = False