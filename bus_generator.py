from bus_factory import BusFactory
import math
import data_loader

network = data_loader.load_network()

def generate_buses(routes, frequencies, capacity):
    buses = [[] for _ in range(len(routes))]
    for k in range(len(routes)):
        bus_factory = BusFactory(network, routes[k])
        bus_number = math.ceil(frequencies[k] * bus_factory.total_time / 30)
        time_delta = math.ceil(3600 / frequencies[k])
        start_time = 0
        for i in range(bus_number):
            new_bus = bus_factory.create_bus(str(k) + str(i),
                                             capacity, start_time)
            buses[k].append(new_bus)
            start_time += time_delta
    return buses

def generate_buses_on_space(routes, frequencies, capacity, arcs):
    buses = [[] for _ in range(len(routes))]
    for k in range(len(routes)):
        bus_factory = BusFactory(network, routes[k])
        bus_number = math.ceil(frequencies[k] * bus_factory.total_time / 30)
        time_delta = math.ceil(3600 / frequencies[k])
        start_time = 0
        for i in range(bus_number):
            new_bus = bus_factory.create_bus(str(k) + str(i),
                                             capacity, start_time)
            current_arc = new_bus.get_arc()
            current_pos = new_bus.get_arc_position()
            while(arcs[current_arc][current_pos]):
                new_bus.starting_time -= 1
                new_bus.starting_time %= 2*new_bus.total_time
                new_bus._set_position_at_time()
                current_arc = new_bus.get_arc()
                current_pos = new_bus.get_arc_position()
            arcs[current_arc][current_pos] = True
            buses[k].append(new_bus)
            start_time += time_delta
    return buses