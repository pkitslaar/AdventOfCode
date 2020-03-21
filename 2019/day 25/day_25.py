import sys
from pathlib import Path
d5_dir = Path(__file__).parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))
from day_05 import run, txt_values

import heapq
import itertools

DROID_MANUAL, DROID_AUTO = range(2)

direction_to_opposite = {
    'north': 'south',
    'south': 'north',
    'east': 'west',
    'west': 'east',
}

class Strategy:
    """
    Base class of strategies, which allows to switch itself into another strategy.
    """

    def switch_to(self, NewStrategy):
        """
        Transforms the current strategy into an instance of the NewStrategy
        """
        print(f'Switching to {NewStrategy}')
        self.__class__ = NewStrategy
        self.__init__()
        return self


class ManualControl(Strategy):
    """
    This is the strategy which allows to manually control the droid.
    """

    def next_command(self, droid, state):
        print(droid.received_txt)
        next_command_valid = False
        command = None
        while not next_command_valid:
            command = input()
            if command.startswith(('take', 'drop', 'inv')) or command in state['doors']:
                next_command_valid = True
            else:
                print('invalid command', command)
        return command

class ExploreStrategy(Strategy):
    """
    This strategy explores all rooms and picks up all 'valid' items in the rooms.

    Valid itesm are items not defined in the ignore items list.
    """

    def __init__(self):
        # Items that should not be picked-up
        self.ignore_items = {'infinite loop', 
                            'escape pod', 
                            'giant electromagnet',
                            'molten lava',
                            'photons',
                            }

    def next_command(self, droid, state):
        """
        Does one of three things
        - pickup any valid item, or
        - go to any unvisited room, or
        - backtrack if all doors in the current room have been visited
        """

        command = None
        # See if there are items to pick-up
        valid_items = set(state['items']) - self.ignore_items
        if valid_items:
            item_to_pickup = list(valid_items)[0]
            command = f'take {item_to_pickup}'
        else:
            # Find next location to explore
            doors_in_room = state['doors']
            non_visited_doors = []
            for d in doors_in_room:            
                if not droid.get_node_in_direction(droid.current_node, d):
                    non_visited_doors.append(d)    
            if non_visited_doors:
                command = non_visited_doors[0]
            else:
                # No more doors to go to so lets go back
                #print('no more doors to visit backtracking')
                if len(droid.route) > 1:
                    prev_room = droid.route[-2]
                    direction = droid.get_direction_for_node(droid.current_node, prev_room)
                    command = direction
                    del droid.route[-1]
                else:
                    print('Visited all rooms')
                    self.switch_to(GoToSecurity)
                    return self.next_command(droid, state)
        return command

class GoToSecurity(Strategy):
    """
    This strategy lets the droid walk from any location in the map
    to the 'Security' room.
    """

    def __init__(self):
        # Holds 'arrival time'/distance map for each room to the 'Security' room.
        self.arrival = None

    def next_command(self, droid, state):
        security_room = 'Security'
        if droid.current_node == security_room:
            print('Reached security room')
            self.switch_to(CrackPressureLock)
            return self.next_command(droid, state)
        else:
            if not self.arrival:
                # Compute the arrival map from the 'Security' room
                self.arrival = droid.propagate(security_room)     
            # Find neighbor with the lowest arrival/distance value
            # This neighbor will bring the droid closer to the target
            neighbor_arrival = [(self.arrival[n],n) for n in droid.get_connected_nodes(droid.current_node)]            
            neighbor_arrival.sort()
            next_room = neighbor_arrival[0][1]

            # Return the direction to walk
            return droid.get_direction_for_node(droid.current_node, next_room)

        return None

class CrackPressureLock(Strategy):
    """
    Strategy to "crack" the pressure lock. 
    For this we need to find the combination of items in 
    the droids inventory that result in the correct weight.

    This is a brute force strategy which tries all possible combinations of items.
    """

    def __init__(self):
        self.initialized = False
        self.permutations_to_check = None
        self.items_to_status = {}

    def initialize(self, droid):
        """
        Compute all combinations of items that the droid can hold.
        Assumes the droid currently hold all the items it has access to.
        """
        current_items_set = tuple(sorted(droid.inventory))
        self.permutations_to_check = {current_items_set}
        for n in range(1,len(current_items_set)+1):
            for comb in itertools.permutations(current_items_set, n):
                self.permutations_to_check.add(tuple(sorted(comb)))
        self.permutations_to_check = list(self.permutations_to_check)
        self.permutations_to_check.sort(key = lambda t: (len(t), t))        

    def next_command(self, droid, state):
        if not self.initialized:
            print('Initializing item permuations')
            self.initialize(droid)    
            self.initialized = True

        if droid.current_node != 'Security':
            print("No longer at security!!!!!!")
            return None

        current_items_set = tuple(sorted(droid.inventory))
        if state.get('analysis_result'):
            # We got back an analysis result, so store it.
            #print(current_items_set, state['analysis_result'][0])
            self.items_to_status[current_items_set] = state
            print('Checked', len(self.items_to_status), 'combinations')
        
        # Remove permutations we have status information for.
        while self.permutations_to_check and self.permutations_to_check[-1] in self.items_to_status:
            self.permutations_to_check.pop()
        if self.permutations_to_check:
            # Define the permutation to check
            perm_to_check = set(self.permutations_to_check[-1])

            # The items the droid currenty holds
            current_set = set(current_items_set)

            # If we miss items, pick-up the missing item
            missing_items = perm_to_check - current_set
            if missing_items:
                return 'take ' + str(list(missing_items)[0])
            # If we have too much items, drop the item we don't need
            redundant_items = current_set - perm_to_check
            if redundant_items:
                return 'drop ' + str(list(redundant_items)[0])
            
            # seems we have the items we want let check at the security
            return "south"
        else:
            # We have exhausted all options, this should not happen
            raise RuntimeError('No more permutations')

class Droid():

    def __init__(self, strategy=ExploreStrategy):
        # Communication
        self.receive_buffer = []
        self.received_txt = None
        self.send_buffer = []

        # State
        self.inventory = []
        self.current_node = None

        # Navigation        
        self.prev_node = None
        self.prev_command = None
        self.route = []

        # Network of rooms
        self.nodes = {}
        self.edges_for_node = {}
        
        # Control strategy
        self.stategy = strategy()
    
    def set_node_for_direction(self, from_node, direction, to_node):
        """
        Store that from_node is connected to to_node in the provided direction.
        Also stores the reverse relationship.
        """
        self.edges_for_node.setdefault(from_node, {})[direction] = to_node
        op_direction = direction_to_opposite[direction]
        self.edges_for_node.setdefault(to_node, {})[op_direction] = from_node

    def get_node_in_direction(self, from_node, direction):
        """
        Returns a node connected to from_node in the given direction.
        Return None if no connection is found or from_node has no connections.
        """
        edges = self.edges_for_node.get(from_node, {})
        return edges.get(direction)

    def get_connected_nodes(self, from_node):
        """
        Returns a list of all nodes connected to from_node
        """
        return list(self.edges_for_node.get(from_node, {}).values())

    def get_direction_for_node(self, from_node, to_node):
        """
        Returns the direction to move to travel between from_node to to_node.
        Returns None if no connection is found.
        """
        edges = self.edges_for_node[from_node]
        for d, node in edges.items():
            if node == to_node:
                return d

    def propagate(self, start_node):
        """
        Construct an arrival time map using 'fast marching' or 'wave propagation'
        algorithm from the provided start_node to all other nodes.
        """
        front = [(0,start_node)]
        heapq.heapify(front)
        arrival = {}
        while front:
            fastest_time, fastest_node = heapq.heappop(front)
            if fastest_node not in arrival:
                arrival[fastest_node] = fastest_time
                connected_nodes = self.get_connected_nodes(fastest_node)                
                for n in connected_nodes:                    
                    if n not in arrival:
                        heapq.heappush(front, (fastest_time+1, n))
        return arrival

    def parse_list(self, lines):
        """
        Extract items lists from the provided input lines.
        Items are lines starting with a dash '-'.

        Used to parse the 'doors', 'items' and 'inventory' output.
        """
        items = []
        for l in lines:
            if l.startswith('- '):
                items.append(l[2:].strip())
            else:
                break
        return items

    def parse_lines(self, splitted_lines):
        """
        Parse the splitted received lines from the program.
        """
        parsed = {}
        if splitted_lines[0].startswith('=='):
            # Room header
            parsed['room'] = splitted_lines[0].split()[1] # name of the room
            parsed['description'] = splitted_lines[1].strip()

            # Find the available doors 
            start_doors = splitted_lines.index('Doors here lead:')
            parsed['doors'] = self.parse_list(splitted_lines[start_doors+1:])

            # See if any items are availble in the room
            try:
                start_items = splitted_lines.index('Items here:')
                parsed['items'] = self.parse_list(splitted_lines[start_items+1:])
            except ValueError:
                parsed['items'] = []

            # In case we are going into the Pressure-Sensitive floor
            # we need to know the Analysis output
            if parsed['description'] == 'Analyzing...':
                start_analysis = start_doors+1+len(parsed['doors'])
                analysis_result = splitted_lines[start_analysis]
                parsed['analysis_result'] = (analysis_result, splitted_lines[start_analysis+1:])
        else:
            # Not a room description
            # let's ses if there is an inventory description
            for key, status in [('inventory', 'Items in your inventory:')]:
                try:
                    start_status = splitted_lines.index(status)
                    parsed[key] = self.parse_list(splitted_lines[start_status+1:])
                except ValueError:
                    pass
        return parsed

    def parse_text(self, txt):
        splitted_lines = [l for l in txt.splitlines() if l.strip()]
        parsed = self.parse_lines(splitted_lines)
        if parsed:
            if 'analysis_result' in parsed:
                result, remaining = parsed['analysis_result']
                sub_parsed = self.parse_lines(remaining)
                parsed['ejected_room'] = sub_parsed
        else:
            all_status = []
            for l in splitted_lines:
                if not l.startswith('Command?'):
                    all_status.append(l)
            parsed['status'] = "\n".join(all_status)
        return parsed

    def next_command(self):
        #print("-"*40)
        try:
            command = None
            parsed = self.parse_text(self.received_txt)
            if 'inventory' in parsed:
                self.inventory = parsed['inventory']
                print(self.inventory)
            status = parsed.get('status', '') 
            if status.startswith("You don't see that item"):
                print(self.received_txt)
                raise RuntimeError()
            elif status.startswith("You don't have that item"):
                print(self.received_txt)
                raise RuntimeError()
            elif status.startswith("You drop the"):
                dropped_item = status[12:-1].strip()
                # automatically call inventory
                #command = 'inv'
                self.nodes[self.current_node]['items'].append(dropped_item)
                self.inventory.remove(dropped_item)
            elif status.startswith("You take the"):
                picked_up_item = status[12:-1].strip()
                # automatically call inventory
                #command = 'inv'
                self.nodes[self.current_node]['items'].remove(picked_up_item)
                self.inventory.append(picked_up_item)

            if 'room' in parsed:                
                self.current_node = parsed['room']
                self.nodes[self.current_node] = parsed                
                if self.prev_command in direction_to_opposite:
                    self.set_node_for_direction(self.prev_node, self.prev_command, self.current_node)
                if not self.route or self.current_node != self.route[-1]:
                    self.route.append(self.current_node)                                        
            if 'ejected_room' in parsed:
                self.current_node = self.route[-2]
                del self.route[-1]
        except Exception:
            print(self.received_txt)
            raise

        if not command:
            current_state = self.nodes[self.current_node]
            state = current_state.copy()
            if 'analysis_result' in parsed:
                state['analysis_result'] = parsed['analysis_result']
            command = self.stategy.next_command(self, state)
        
        #print(self.current_node, 'next command', command)
        # Fill the send buffer with the int characters and end with 10
        # The buffer is filled in reverse order so we can easily call
        # pop() to send each character
        self.send_buffer = list(reversed([ord(c) for c in command] + [10]))

        self.prev_command = command
        self.prev_node = self.current_node
        

    def update_receive_txt(self):
        """
        Converts the received int characters to actual text string.
        """
        if self.receive_buffer:
            self.received_txt = ''.join(chr(v) for v in self.receive_buffer)
            self.receive_buffer = []

    def send(self):
        """
        Should send the next command a character at a time.
        
        This is also the signal that all data is received and the
        next command can be defined.
        """
        if self.receive_buffer:
            # If we still have received data to process
            # do this now
            self.update_receive_txt()
            # Compute the next commandß
            self.next_command()
        
        if self.send_buffer:
            # While we have data in the send buffer
            # send them a character at a time
            v = self.send_buffer.pop()
            return v

    def receive(self, v):    
        """
        Receives a single character at a time, so we put them in a buffer.
        """    
        self.receive_buffer.append(v)

if __name__ == "__main__":
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_program = txt_values(f.read())
    
    # Use the ManualControl stategy to control the droid manually
    #d = Droid(ManualControl)

    # This setup automatically solves the puzzle
    d = Droid(ExploreStrategy)
    
    run(main_program, input_v=d.send, output_cb=d.receive, stop_on_output=False)
    d.update_receive_txt()
    print(d.received_txt)
