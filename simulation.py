from bus_generator import generate_buses_on_space
from passenger_generator import generate_passengers, generate_passengers_test
from platform_generator import generate_platforms
from logger import save_state_data, save_to_csv, save_arcflows, get_max_arcflow
import datetime
import itertools
import data_loader
import arc_manager

# Global variables
coordinates = data_loader.load_coordinates()
network = data_loader.load_network()
arc_positions = arc_manager.create_arcs()
arc_coordinates = arc_manager.create_arc_coordinates()

# Constants
STATION_NUMBER = len(network)
MAX_TIME_SIMULATED = 5000000
TRANSFER_TIME = 5 * 60

bus_positions = []
bus_occupancies = []
bus_speeds = []
route_slowest_arc = []
route_bus_number = []
arc_people_count = {(i, j):[] for i, l in enumerate(network) for j, _ in l}
passengers_at_time = [0] * MAX_TIME_SIMULATED
stations = [set() for _ in range(STATION_NUMBER)]
platforms = generate_platforms(STATION_NUMBER)
data_loader.load_platforms()
def generate_entities(network_routes, network_stops, network_frequencies, capacities):
    global bus_occupancies, bus_speeds, route_bus_number, route_slowest_arc
    passengers = generate_passengers(network_routes, network_stops, stations, passengers_at_time)
    bus_routes = generate_buses_on_space(network_routes, network_stops, network_frequencies, capacities, arc_positions, platforms)
    passengers_pref_time = list(itertools.accumulate(passengers_at_time))
    bus_occupancies = [[] for _ in bus_routes]
    bus_speeds = [[] for _ in bus_routes]
    route_slowest_arc = [[] for _ in bus_routes]
    route_bus_number = [len(route) for route in bus_routes]
    return passengers, bus_routes, passengers_pref_time

def update_bus_status(bus_routes, bus_capacities, time, passengers, on_bus, t_time):
    global bus_positions, arc_positions, stations, bus_occupancies, bus_speeds, route_bus_number, route_slowest_arc
    current_positions = []
    for route_idx, route in enumerate(bus_routes):
        total_occupancy = 0
        total_speed = 0
        route_arcs = {}
        for bus_idx, bus in enumerate(route):
            total_occupancy += bus_capacities[route_idx] - bus.capacity
            total_speed += bus.get_last_avg_speed()
            alighted_passengers, transfered_passengers, new_passengers = bus.move(arc_positions, stations, passengers, platforms, time)
            on_bus -= alighted_passengers
            t_time += TRANSFER_TIME * transfered_passengers
            on_bus += new_passengers
            current_arc = bus.get_arc()
            if current_arc in route_arcs:
                xn, n = route_arcs[current_arc][0], route_arcs[current_arc][1]
                route_arcs[current_arc][0] = xn + (bus.get_last_avg_speed()-xn)/n
                route_arcs[current_arc][1] += 1
            else:
                route_arcs[current_arc] = [bus.get_last_avg_speed(), 1]
                
            if(bus.previous_state and bus.previous_state["arc"] != current_arc):
                arc_people_count[current_arc].append((time, bus_capacities[route_idx] - bus.capacity))
            
            if(bus.state == 'on_station'):
                current_positions.append(coordinates[bus.current_node])
            else:
                pos = bus.get_arc_position()
                lane = bus.lane
                current_positions.append(arc_coordinates[current_arc][lane][pos])
        min_val = 1000
        min_arc = (0,0)
        for arc, speed in route_arcs.items():
            if speed[0] < min_val:
                min_val = speed[0]
                min_arc = arc
        bus_occupancies[route_idx].append(total_occupancy/(bus_capacities[route_idx]*route_bus_number[route_idx]))
        bus_speeds[route_idx].append(total_speed/route_bus_number[route_idx])
        route_slowest_arc[route_idx].append((min_val, min_arc))
        
    bus_positions.append(current_positions)
    return on_bus, t_time

def update_times(passengers_pref_time, on_bus, time, n, passengers, w_time, inv_time):
    inactives = n - len(passengers)
    w_time += passengers_pref_time[time] - on_bus - inactives
    inv_time += on_bus
    return w_time, inv_time

def run_simulation(network_routes, network_stops, network_frequencies, capacities, visualize=False, save_metrics=False):
    passengers, bus_routes, passengers_pref_time = generate_entities(network_routes, network_stops, network_frequencies, capacities)
    print(len(passengers))
    t_s = datetime.datetime.now()
    n = len(passengers)
    inv_time, t_time, w_time, on_bus = 0, 0, 0, 0
    time = 0
    total_dist = 0
    for node in network:
        for a,c in node:
            total_dist += c
    #print(total_dist//2*15)
    while len(passengers) > 0:
        on_bus, t_time = update_bus_status(bus_routes, capacities, time, passengers, on_bus, t_time)
        w_time, inv_time = update_times(passengers_pref_time, on_bus, time, n, passengers, w_time, inv_time)
        time += 1
        
        if save_metrics:
            save_state_data(bus_routes, time, capacities)
        
    if save_metrics:
        save_to_csv()
        save_arcflows(arc_people_count, f"results/flow_data_{data_loader.INSTANCE_NAME}.csv", 24)
        
    print_results(time, inv_time, w_time, t_time)
    t_e = datetime.datetime.now()
    print(t_e - t_s)
    if visualize:
        import visualization
        visualization.visualize_simulation(bus_positions, bus_routes, coordinates, network, bus_occupancies, bus_speeds, route_slowest_arc, skip_frames=1)

def evaluate(network_routes, network_stops, network_frequencies, capacities):
    passengers, bus_routes, passengers_pref_time = generate_entities(network_routes, network_stops, network_frequencies, capacities)
    n = len(passengers)
    inv_time, t_time, w_time, on_bus = 0, 0, 0, 0
    time = 0
    while len(passengers) > 0:
        on_bus, t_time = update_bus_status(bus_routes, capacities, time, passengers, on_bus, t_time)
        w_time, inv_time = update_times(passengers_pref_time, on_bus, time, n, passengers, w_time, inv_time)
        time += 1
    inv_time //= 60
    w_time //= 60
    t_time //= 60
    total_time = inv_time + w_time + t_time
    return time, inv_time, w_time, t_time, total_time, get_max_arcflow(arc_people_count, 24)

def print_results(time, inv_time, w_time, t_time):
    print(time)
    print(inv_time // 60, w_time // 60, t_time // 60, (inv_time + w_time + t_time) // 60)

# Simulation parameters
network_routes = data_loader.load_routes()
network_stops = data_loader.load_stops()
network_frequencies = data_loader.load_frequencies()
network_capacities = data_loader.load_capacities()

# Run the simulation with visualization enabled
#run_simulation(network_routes, network_stops, network_frequencies, network_capacities, visualize=True, save_metrics=True)
print(evaluate(network_routes, network_stops, network_frequencies, network_capacities))
#get_transfers_routes(43, 28, network_routes)

#instance 5:
#total: 7130984
#inv, wt, tt = 2362312 4768671 0
#buses = 268

#instance 6:
#total: 3915237
#inv, wt, tt = 1737249 2177987 0
#buses = 172

#instance 7:
#total: 6718203
#inv, wt, tt = 1695982 5022220 0
#buses = 201
