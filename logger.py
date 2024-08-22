import pandas as pd
import itertools
import numpy as np

bus_data = {
        'bus_id': [],
        'route_id': [],
        'time': [],
        'passenger_count': [],
        'speed': [],
        'arc': []
    }

def save_state_data(bus_routes, t, total_bus_capacities):
    for r_idx, route in enumerate(bus_routes):
        for bus in route:
            bus_data['bus_id'].append(bus.id)
            bus_data['route_id'].append(bus.route_id)
            bus_data['time'].append(t)
            bus_data['passenger_count'].append(total_bus_capacities[r_idx] - bus.capacity)
            bus_data['speed'].append(bus.speed)
            bus_data['arc'].append(bus.get_arc())
            
    
def save_to_csv(save_location = "results/bus_data.csv"):
    df = pd.DataFrame(bus_data)
    df.to_csv(save_location, index=False)
    
def save_flow_tables(arc_data, total_simulation_time, n, interval_size = 3600, interval_step = 900, save_location = "results/"):
    for arc in arc_data:
        arc_data[arc] = list(itertools.accumulate(arc_data[arc]))
    assert(total_simulation_time >= interval_size)
    steps = (total_simulation_time - interval_size)//interval_step
    file_name = save_location + 'passenger_flow_'
    for i in range(steps):
        arc_flows = np.zeros((n, n), dtype=int)
        for arc in arc_data:
            a, b = arc
            arc_flows[a, b] = arc_data[arc][interval_size + interval_step*i] - arc_data[arc][interval_step*i]
        df = pd.DataFrame(arc_flows)
        df.to_csv(file_name + str(i) + '.csv', index = False)