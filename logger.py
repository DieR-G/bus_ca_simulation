import pandas as pd

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