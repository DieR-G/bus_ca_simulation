import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def visualize_simulation(bus_positions, bus_routes, coordinates, network, skip_frames=1):
    fig, ax = plt.subplots()
    ax.set_xlim(min([c[0] for c in coordinates]) - 10, max([c[0] for c in coordinates]) + 10)
    ax.set_ylim(min([c[1] for c in coordinates]) - 10, max([c[1] for c in coordinates]) + 10)

    # Plot network connections
    for i, connections in enumerate(network):
        for j, _ in connections:
            start = coordinates[i]
            end = coordinates[j]
            ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', lw=0.5)

    # Plot nodes with larger size and purple color
    ax.plot([c[0] for c in coordinates], [c[1] for c in coordinates], 'o', color='red', markersize=5)

    # Define custom colors for the routes
    custom_colors = ['blue', 'orange', 'magenta', 'purple']

    # Create bus markers for each route
    buses = []
    for route_index, route in enumerate(bus_routes):
        route_color = custom_colors[route_index % len(custom_colors)]  # Cycle through custom colors
        route_buses = [ax.plot([], [], 'o', color=route_color, markersize=4)[0] for _ in route]
        buses.extend(route_buses)

    def init():
        for bus in buses:
            bus.set_data([], [])
        return buses

    def update(frame):
        positions = bus_positions[frame * skip_frames]  # Skip frames to speed up animation
        for bus, pos in zip(buses, positions):
            bus.set_data([pos[0]], [pos[1]])  # Pass coordinates as lists
        return buses

    ani = animation.FuncAnimation(
        fig, update, frames=range(0, len(bus_positions) // skip_frames), init_func=init,
        blit=True, interval=30, repeat=False  # Adjust interval as needed
    )
    plt.show()
