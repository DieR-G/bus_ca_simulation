import data_loader

routes = data_loader.load_routes()
platforms_data = data_loader.load_platforms()
PLATFORM_NUMBER = 10

def generate_platforms(stations_number):
    stations = [{} for _ in range(stations_number)]
    platforms = [[[],[]] for _ in range(stations_number)]
    for node, platform_list in enumerate(platforms_data):
        for list in platform_list:
            platforms[node][0].append([True, set(list)])
            platforms[node][1].append([True, set(list)])
    for r_idx, route in enumerate(routes):
        for node in route:
            stations[node][r_idx] = [PLATFORM_NUMBER, PLATFORM_NUMBER]
    return platforms