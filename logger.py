import pandas as pd
import numpy as np

data = {
        'bus_id': [],
        'route_id': [],
        'time': [],
        'passenger_count': [],
        'speed': []
    }

def save_state_data(bus_routes, t, total_bus_capacity):
    for route in bus_routes:
        for bus in route:
            data['bus_id'].append(bus.id)
            data['route_id'].append(bus.route_id)
            data['time'].append(t)
            data['passenger_count'].append(total_bus_capacity - bus.capacity)
            data['speed'].append(bus.speed)
    
    

def save_to_csv(save_location = "results/bus_data.csv"):
    df = pd.DataFrame(data)
    df.to_csv(save_location, index=False)