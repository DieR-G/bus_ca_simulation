import json

COORDINATES_PATH = 'data/coordinates.json'
DEMAND_MATRIX_PATH = 'data/demand_matrix.json'
NETWORK_PATH = 'data/network.json'
ROUTES_PATH = 'data/routes.json'
FREQUENCIES_PATH = 'data/frequencies.json'

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

def load_frequencies():
    with open(FREQUENCIES_PATH, 'r') as file:
        frequencies = json.load(file)
    return frequencies