class Bus:
    def __init__(self, id, route, route_id, capacity, starting_time, total_time, node_time_map, index_time_list):
        """
        Initialize a Bus instance

        ### Parameters:
        - `id` (int): Identifier of the bus
        - `route` (list): List of nodes representing the bus route
        - `capacity` (int): Capacity of the bus
        - `starting_time` (int): The starting time of the bus in seconds
        - `total_time` (int): Total time for one round trip in minutes
        - `node_time_map` (dict): Dictionary mapping positions to node times
        - `index_time_list` (list): List of times for each index position on the route
        """
        self.id = id
        self.route = route
        self.route_id = route_id
        self.capacity = capacity
        self.route_position = 1
        self.direction = 1
        self.current_node = route[0]
        self.state = "on_station"
        self.position = 0
        self.stop_time = 0
        self.starting_time = starting_time
        self.node_time_map = node_time_map
        self.index_time_list = index_time_list
        self.total_time = 60 * total_time  # Convert total_time to seconds
        self._set_position_at_time()
        self.stations_map = {i: [] for i in self.route}
        self.lane = 0
        self.previous_state = None
        self.bus_ahead = None
    def __str__(self):
        """
        String representation of the Bus

        ### Returns:
        - `str`: A string describing the current state of the bus
        """
        return f"Bus {self.id} at: {self.position}, capacity: {self.capacity}"

    def save_prev_state(self):
        self.previous_state = {
            "position": self.position,
            "route_position": self.route_position,
            "direction": self.direction,
            "current_node": self.current_node,
            "state": self.state
        }
    
    def _move(self):
        """
        Move the bus one position in its current direction on the network
        """        
        self.position += self.direction
        if self.position in self.node_time_map:
            self.state = "on_station"
            self.current_node = self.node_time_map[self.position]
            self._update_position()
        else:
            self.state = "on_road"

    def move(self, arc_positions, stations, passengers, platforms, time):
        alighted_passengers, transfered_passengers, new_passengers = 0, 0, 0
        self.save_prev_state()
        if self.stop_time > 0:
            self.stop_time -= 1
            return alighted_passengers, transfered_passengers, new_passengers
        
        platform_direction = lambda x: 0 if x == 1 else 1

        if self.state == "on_station":
            platforms[self.current_node][self.route_id][platform_direction(self.direction)] = ""

        arc_positions[self.get_arc()][self.lane][self.get_arc_position()] = ""
        self._move()
        if self.state == "on_station" and platforms[self.current_node][self.route_id][platform_direction(self.direction)] != "":
            self.undo_move()
            arc_positions[self.get_arc()][self.lane][self.get_arc_position()] = self.id
            return alighted_passengers, transfered_passengers, new_passengers
        
        if arc_positions[self.get_arc()][self.lane][self.get_arc_position()] != "" and self.state == 'on_road':
            self.undo_move()
            if self.state == "on_station":
                platforms[self.current_node][self.route_id][platform_direction(self.direction)] = self.id
            
            if (self.bus_ahead.current_node != self.current_node and 
                    arc_positions[self.get_arc()][1][self.get_arc_position()] == ""):
                self.lane = 1
            
            arc_positions[self.get_arc()][self.lane][self.get_arc_position()] = self.id
            
            return alighted_passengers, transfered_passengers, new_passengers
        
        if self.state == "on_station":
            self.lane = 0
            platforms[self.current_node][self.route_id][platform_direction(self.direction)] = self.id
            self.stop_time = 30
            alighted_passengers, transfered_passengers = self.alight_passengers(stations, passengers)
            new_passengers = self.board_passengers(stations, time)
                 
        arc_positions[self.get_arc()][self.lane][self.get_arc_position()] = self.id
        return alighted_passengers, transfered_passengers, new_passengers

    def undo_move(self):
        if self.previous_state:
            self.position = self.previous_state["position"]
            self.route_position = self.previous_state["route_position"]
            self.direction = self.previous_state["direction"]
            self.current_node = self.previous_state["current_node"]
            self.state = self.previous_state["state"]
        else:
            print("No move to undo")

    def _update_position(self):
        """
        Update the bus position within the route

        Change direction if necessary.
        """
        if self.route_position + self.direction >= len(self.route) or self.route_position + self.direction < 0:
            self.direction *= -1
        self.route_position += self.direction

    def _in_bounds(self, val):
        """
        Ensure a value is within the bounds of the route list

        ### Parameters:
        - `val` (int): The value to check

        ### Returns:
        - `int`: The bounded value
        """
        return max(0, min(val, len(self.route) - 1))

    def get_last_node(self):
        """
        Get the last node on the route

        ### Returns:
        - `object`: The last node
        """
        return self.route[self._in_bounds(self.route_position - self.direction)]

    def get_next_node(self):
        """
        Get the next node on the route

        ### Returns:
        - `object`: The next node
        """
        return self.route[self._in_bounds(self.route_position)]

    def get_last_index(self):
        """
        Get the last index on the route

        ### Returns:
        - `int`: The last index
        """
        return self._in_bounds(self.route_position - self.direction)

    def get_next_index(self):
        """
        Get the next index on the route

        ### Returns:
        - `int`: The next index
        """
        return self._in_bounds(self.route_position)

    def get_arc(self):
        """
        Get the current arc (last and next nodes)

        ### Returns:
        - `tuple`: A tuple containing the last and next nodes
        """
        return self.get_last_node(), self.get_next_node()

    def get_arc_position(self):
        """
        Get the position within the current arc

        ### Returns:
        - `int`: The position within the arc
        """
        return self.direction*(self.position - self.index_time_list[self.get_last_index()])

    def _binary_search(self, condition):
        """
        Perform a binary search based on the given condition

        ### Parameters:
        - `condition` (function): A lambda function to evaluate the condition

        ### Returns:
        - `int`: The index satisfying the condition
        """
        low, high = 0, len(self.route) - 1
        while low < high:
            mid = (low + high) // 2
            if condition(mid):
                high = mid
            else:
                low = mid + 1
        return low

    def _get_position_at_time(self, t):
        """
        Determine the position of the bus at a given time

        ### Parameters:
        - `t` (int): The time in seconds

        ### Returns:
        - `tuple`: A tuple of (current index, next index)
        """
        if t >= self.total_time:
            t -= self.total_time
            idx = self._binary_search(lambda x: self.index_time_list[-1] - self.index_time_list[x] < t)
            self.direction = -1
        else:
            idx = self._binary_search(lambda x: self.index_time_list[x] > t)
            idx -= 1
        next_idx = idx + self.direction
        return idx, next_idx

    def _set_position_at_time(self):
        """
        Set the bus position based on a given time

        ### Parameters:
        - `t` (int): The time in seconds
        """
        t = self.starting_time
        t %= 2 * self.total_time
        at_idx, next_idx = self._get_position_at_time(t)
        self.route_position = next_idx
        self.state = "on_station"
        self.current_node = self.route[at_idx]
        if 2 * self.total_time - t in self.node_time_map:
            self.direction = -1
        elif t not in self.node_time_map:
            self.state = "on_road"
        self.position = t if self.direction > 0 else 2 * self.total_time - t

    def alight_passengers(self, stations, passengers):
        """
        Processes the alighting of passengers

        ### Parameters:
        - `stations` (list): A list of list, where each sub list stores the passengers on that stations
        - `passengers` (list): Global list of passengers
        """
        passenger_number, transfer_num = 0, 0
        for passenger in self.stations_map[self.current_node]:
            passenger.current_bus = "-1"
            passenger.current_station = passenger.path[passenger.path_pos]
            passenger.path_pos -= 1
            if passenger.path_pos < 0:
                passengers.remove(passenger)
                continue
            stations[passenger.current_station].add(passenger)
            transfer_num += 1
        passenger_number = len(self.stations_map[self.current_node])
        self.capacity += passenger_number
        self.stations_map[self.current_node] = []
        return passenger_number, transfer_num

    def board_passengers(self, stations, t):
        new_passengers = 0
        to_remove = []
        for passenger in stations[self.current_node]:
            if passenger.arrival_time > t:
                continue
            if self.capacity > 0:
                to = self.route[self.route_position:] if self.direction > 0 else self.route[:self.route_position + 1]
                if passenger.path[passenger.path_pos] in to:
                    passenger.current_bus = self.id
                    self.capacity -= 1
                    new_passengers += 1
                    self.stations_map[passenger.path[passenger.path_pos]].append(passenger)
                    to_remove.append(passenger)  # Add passenger to the removal list
            else:
                break
        for passenger in to_remove:
            stations[self.current_node].discard(passenger)
        return new_passengers