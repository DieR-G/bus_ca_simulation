from bus_generator import generate_buses_on_space
from passenger_generator import generate_passengers_test
import datetime
import itertools
import data_loader
import arc_manager

# Constants
STATION_NUMBER = 15
MAX_TIME_SIMULATED = 50000
TRANSFER_TIME = 5 * 60

# Global variables
coordinates = data_loader.load_coordinates()
network = data_loader.load_network()
arc_positions = arc_manager.create_arcs()
arc_coordinates = arc_manager.create_arc_coordinates()
bus_positions = []
passengers_at_time = [0] * MAX_TIME_SIMULATED
stations = [set() for _ in range(STATION_NUMBER)]
platforms = [4]*STATION_NUMBER

def generate_entities(network_routes, network_frequencies, CAP):
    passengers = generate_passengers_test(network_routes, stations, passengers_at_time)
    bus_routes = generate_buses_on_space(network_routes, network_frequencies, CAP, arc_positions, platforms)
    passengers_pref_time = list(itertools.accumulate(passengers_at_time))
    return passengers, bus_routes, passengers_pref_time, stations

def update_bus_status(bus_routes, time, passengers, on_bus, t_time):
    global bus_positions, arc_positions, stations
    current_positions = []
    for route in bus_routes:
        for bus in route:
            alighted_passengers, transfered_passengers, new_passengers = bus.move(arc_positions, stations, passengers, platforms, time)
            on_bus -= alighted_passengers
            t_time += TRANSFER_TIME * transfered_passengers
            on_bus += new_passengers
            if(bus.state == 'on_station'):
                current_positions.append(coordinates[bus.current_node])
            else:
                arc = bus.get_arc()
                pos = bus.get_arc_position()
                lane = bus.lane
                current_positions.append(arc_coordinates[arc][lane][pos])
    bus_positions.append(current_positions)
    return on_bus, t_time

def update_times(passengers_pref_time, on_bus, time, n, passengers, w_time, inv_time):
    inactives = n - len(passengers)
    w_time += passengers_pref_time[time] - on_bus - inactives
    inv_time += on_bus
    return w_time, inv_time

def run_simulation(network_routes, network_frequencies, CAP, visualize=False):
    passengers, bus_routes, passengers_pref_time, stations = generate_entities(network_routes, network_frequencies, CAP)
    print(len(passengers))
    t_s = datetime.datetime.now()
    n = len(passengers)
    inv_time, t_time, w_time, on_bus = 0, 0, 0, 0
    time = 0

    while len(passengers) > 0:
        on_bus, t_time = update_bus_status(bus_routes, time, passengers, on_bus, t_time)
        w_time, inv_time = update_times(passengers_pref_time, on_bus, time, n, passengers, w_time, inv_time)
        time += 1

    print_results(time, inv_time, w_time, t_time)
    t_e = datetime.datetime.now()
    print(t_e - t_s)
    
    if visualize:
        import visualization
        visualization.visualize_simulation(bus_positions, bus_routes, coordinates, network, skip_frames=5)

def print_results(time, inv_time, w_time, t_time):
    print(time)
    print(inv_time // 60, w_time // 60, t_time // 60, (inv_time + w_time + t_time) // 60)

# Simulation parameters
CAP = 50

network_routes = data_loader.load_routes()
network_frequencies = data_loader.load_frequencies()

# Run the simulation with visualization enabled
run_simulation(network_routes, network_frequencies, CAP, visualize=True)
