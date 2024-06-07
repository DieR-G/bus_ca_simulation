import json

def load_coordinates():
    with open('data/coordinates.json', 'r') as file:
        coordinates = json.load(file)
    return coordinates

def load_demand_matrix():
    with open('data/demand_matrix.json', 'r') as file:
        demand_matrix = json.load(file)
    return demand_matrix

def load_network():
    with open('data/network.json', 'r') as file:
        network = json.load(file)
    return network    