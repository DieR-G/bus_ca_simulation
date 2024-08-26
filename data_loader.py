import json

COORDINATES_PATH = 'data/coordinates4.json'
DEMAND_MATRIX_PATH = 'data/demand_matrix4.json'
NETWORK_PATH = 'data/network4.json'
ROUTES_PATH = 'data/routes4.json'
STOPS_PATH = 'data/stops4.json'
FREQUENCIES_PATH = 'data/frequencies4.json'
CAPACITIES_PATH = 'data/capacities4.json'

def load_coordinates():
    with open(COORDINATES_PATH, 'r') as file:
        coordinates = json.load(file)
    return coordinates

def load_demand_matrix():
    with open(DEMAND_MATRIX_PATH, 'r') as file:
        demand_matrix = json.load(file)
    return demand_matrix

def load_network():
    with open(NETWORK_PATH, 'r') as file:
        network = json.load(file)
    return network    

def load_routes():
    with open(ROUTES_PATH, 'r') as file:
        routes = json.load(file)
    return routes

def load_stops():
    with open(STOPS_PATH, 'r') as file:
        stops = json.load(file)
    return stops

def load_frequencies():
    with open(FREQUENCIES_PATH, 'r') as file:
        frequencies = json.load(file)
    return frequencies

def load_capacities():
    with open(CAPACITIES_PATH, 'r') as file:
        capacities = json.load(file)
    return capacities