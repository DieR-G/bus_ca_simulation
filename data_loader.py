import json

INSTANCE_NAME = '403k_q2'
INSTANCE_PATH='data/instance_' + INSTANCE_NAME

COORDINATES_PATH = INSTANCE_PATH + '/coordinates.json'
DEMAND_MATRIX_PATH = INSTANCE_PATH + '/demand_matrix.json'
NETWORK_PATH = INSTANCE_PATH + '/network.json'
ROUTES_PATH = INSTANCE_PATH + '/routes.json'
STOPS_PATH = INSTANCE_PATH + '/stops.json'
FREQUENCIES_PATH = INSTANCE_PATH + '/frequencies.json'
CAPACITIES_PATH = INSTANCE_PATH + '/capacities.json'
PLATFORMS_PATH = INSTANCE_PATH + '/platforms.json'

def load_path(path):
    with open(path, 'r') as file:
        val = json.load(file)
    return val

def load_coordinates():
    return load_path(COORDINATES_PATH)

""" nodes = [0] * len(demand_matrix)
    h = []
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix)):
            nodes[j] += demand_matrix[i][j]
    for i in range(len(demand_matrix)):
        pq.heappush(h, (nodes[i], i))
    print(pq.nlargest(15, h)) """

def load_demand_matrix():
    return load_path(DEMAND_MATRIX_PATH)

def load_network():
    return load_path(NETWORK_PATH)

def load_routes():
    return load_path(ROUTES_PATH)

def load_stops():
    return load_path(STOPS_PATH)

def load_frequencies():
    return load_path(FREQUENCIES_PATH)

def load_capacities():
    return load_path(CAPACITIES_PATH)

def load_platforms():
    return load_path(PLATFORMS_PATH)