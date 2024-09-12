import json
import heapq as pq

INSTANCE_PATH=  'data/instance7'

COORDINATES_PATH = INSTANCE_PATH + '/coordinates.json'
DEMAND_MATRIX_PATH = INSTANCE_PATH + '/demand_matrix.json'
NETWORK_PATH = INSTANCE_PATH + '/network.json'
ROUTES_PATH = INSTANCE_PATH + '/routes.json'
STOPS_PATH = INSTANCE_PATH + '/stops.json'
FREQUENCIES_PATH = INSTANCE_PATH + '/frequencies.json'
CAPACITIES_PATH = INSTANCE_PATH + '/capacities.json'

def load_coordinates():
    with open(COORDINATES_PATH, 'r') as file:
        coordinates = json.load(file)
    return coordinates


""" nodes = [0] * len(demand_matrix)
    h = []
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix)):
            nodes[j] += demand_matrix[i][j]
    for i in range(len(demand_matrix)):
        pq.heappush(h, (nodes[i], i))
    print(pq.nlargest(15, h)) """

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