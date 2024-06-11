from bus_generator import generate_buses
from passenger_generator import generate_passengers_test
import datetime
import itertools
import data_loader
import arc_manager
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import get_cmap

# Constants
STATION_NUMBER = 15
MAX_TIME_SIMULATED = 10000
TRANSFER_TIME = 5 * 60

# Global variables
station_passengers_history = []
time_history = []
coordinates = data_loader.load_coordinates()
network = data_loader.load_network()
arc_positions = arc_manager.create_arcs()
arc_coordinates = arc_manager.create_arc_coordinates()
bus_positions = []

def initialize_simulation():
    passengers_at_time = [0] * MAX_TIME_SIMULATED
    stations = [set() for _ in range(STATION_NUMBER)]
    return passengers_at_time, stations

def generate_entities(network_routes, network_frequencies, CAP):
    passengers_at_time, stations = initialize_simulation()
    passengers = generate_passengers_test(network_routes, stations, passengers_at_time)
    bus_routes = generate_buses(network_routes, network_frequencies, CAP)
    passengers_pref_time = list(itertools.accumulate(passengers_at_time))
    return passengers, bus_routes, passengers_pref_time, stations

def update_bus_status(bus_routes, time, arc_positions, stations, passengers, on_bus, t_time):
    global bus_positions
    current_positions = []
    for route in bus_routes:
        for bus in route:
            alighted_passengers, transfered_passengers, new_passengers = bus.move(arc_positions, stations, passengers, time)
            on_bus -= alighted_passengers
            t_time += TRANSFER_TIME * transfered_passengers
            on_bus += new_passengers
            arc = bus.get_arc()
            pos = bus.get_arc_position()
            current_positions.append(arc_coordinates[arc][pos])
    bus_positions.append(current_positions)
    return on_bus, t_time

def update_times(passengers_pref_time, on_bus, time, n, passengers, w_time, inv_time):
    inactives = n - len(passengers)
    w_time += passengers_pref_time[time] - on_bus - inactives
    inv_time += on_bus
    return w_time, inv_time

def run_simulation(network_routes, network_frequencies, CAP):
    passengers, bus_routes, passengers_pref_time, stations = generate_entities(network_routes, network_frequencies, CAP)
    print(len(passengers))
    t_s = datetime.datetime.now()
    n = len(passengers)
    inv_time, t_time, w_time, on_bus = 0, 0, 0, 0
    time = 0

    while len(passengers) > 0:
        on_bus, t_time = update_bus_status(bus_routes, time, arc_positions, stations, passengers, on_bus, t_time)
        w_time, inv_time = update_times(passengers_pref_time, on_bus, time, n, passengers, w_time, inv_time)
        time += 1

    print_results(time, inv_time, w_time, t_time)
    t_e = datetime.datetime.now()
    print(t_e - t_s)
    visualize_simulation(bus_positions, bus_routes)

def print_results(time, inv_time, w_time, t_time):
    print(time)
    print(inv_time // 60, w_time // 60, t_time // 60, (inv_time + w_time + t_time) // 60)

def visualize_simulation(bus_positions, bus_routes):
    fig, ax = plt.subplots()
    ax.set_xlim(min([c[0] for c in coordinates]) - 10, max([c[0] for c in coordinates]) + 10)
    ax.set_ylim(min([c[1] for c in coordinates]) - 10, max([c[1] for c in coordinates]) + 10)

    # Plot network connections
    for i, connections in enumerate(network):
        for j, _ in connections:
            start = coordinates[i]
            end = coordinates[j]
            ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', lw=0.5)

    # Plot nodes
    ax.plot([c[0] for c in coordinates], [c[1] for c in coordinates], 'ro')

    # Use a colormap to assign different colors to each route
    cmap = get_cmap('tab10')
    route_colors = [cmap(i) for i in range(len(bus_routes))]

    # Create bus markers for each route
    buses = []
    bus_route_indices = []
    for route_index, route_color in enumerate(route_colors):
        route_buses = [ax.plot([], [], 'o', color=route_color, markersize=5)[0] for _ in bus_routes[route_index]]
        buses.extend(route_buses)
        bus_route_indices.extend([route_index] * len(route_buses))

    def init():
        for bus in buses:
            bus.set_data([], [])
        return buses

    def update(frame):
        positions = bus_positions[frame]
        for bus, pos in zip(buses, positions):
            bus.set_data([pos[0]], [pos[1]])  # Pass coordinates as lists
        return buses

    ani = animation.FuncAnimation(fig, update, interval=30, frames=range(len(bus_positions)), init_func=init, blit=True, repeat=False)
    plt.show()

# Simulation parameters
CAP = 50

network_routes = [
    [0, 1, 2, 6], [3, 4, 5, 6],
    [6, 7, 8, 9, 10], [9, 10, 11, 12, 13, 14]
]
network_frequencies = [16.18, 17.02, 26.64, 19.94]

# Run the simulation
run_simulation(network_routes, network_frequencies, CAP)
