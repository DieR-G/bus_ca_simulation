import data_loader

routes = data_loader.load_routes()

def generate_platforms(stations_number):
    stations = [{} for _ in range(stations_number)]
    for r_idx, route in enumerate(routes):
        for node in route:
            stations[node][r_idx] = ["",""]
    return stations