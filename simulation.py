from bus_generator import generate_buses
from passenger_generator import generate_passengers_test
import datetime
import itertools
import data_loader
import arc_manager

STATION_NUMBER = 15
MAX_TIME_SIMULATED = 10000
TRANSFER_TIME = 5*60

station_passengers_history = []
time_history = []
coordinates = data_loader.load_coordinates()
network = data_loader.load_network()
arc_positions = arc_manager.create_arcs()

def simulate(network_frequencies, network_routes, CAP):    
    passengers_at_time = [0]*MAX_TIME_SIMULATED
    stations = [set() for _ in range(STATION_NUMBER)]
    passengers = generate_passengers_test(network_routes, stations, passengers_at_time)
    bus_routes = generate_buses(network_routes, network_frequencies, CAP)
    passengers_pref_time = list(itertools.accumulate(passengers_at_time))
    print(len(passengers))
    t_s = datetime.datetime.now()
    n = len(passengers)
    inv_time = 0
    t_time = 0
    w_time = 0
    on_bus = 0               
    time = 0
    while len(passengers) > 0:
        for route in bus_routes:
            for bus in route:
                alighted_passengers, transfered_passengers, new_passengers = 0, 0, 0
                alighted_passengers, transfered_passengers, new_passengers = bus.move(arc_positions, stations, passengers, time)
                on_bus -= alighted_passengers
                t_time += TRANSFER_TIME*transfered_passengers
                on_bus += new_passengers
        inactives = n - len(passengers)
        w_time += passengers_pref_time[time] - on_bus - inactives
        inv_time += on_bus
        time += 1
    print(time)
    print(inv_time//60, w_time//60, t_time//60, (inv_time+w_time+t_time)//60)
    t_e = datetime.datetime.now()
    print(t_e-t_s)
    
CAP = 50

""" network_routes = [[0,1,2,5,7,9,10,12], [4,3,5,7,14,6], [11,3,5,14,8],[9,13,12]]
network_frequencies = [68.2, 19.900000000000002, 15.210936746793037, 5.446410882717701] 
 """
 
network_routes = [[0,1,2,6],[3,4,5,6],[6,7,8,9,10],[9,10,11,12,13,14]]
network_frequencies = [16.18, 17.02, 26.64, 19.94]
""" network_routes = [[10,12,13,9,7,14,5,2,1,0],[6,14,5,3,4],[11,3,5,14,8]]
network_frequencies = [68.5, 19.900000000000002, 16.45525002610718] """

""" network_routes = [[0,1,2,5,7,9,10]]
network_frequencies = [10] 
simulation_time = 5580
"""

simulate(network_frequencies, network_routes, CAP)