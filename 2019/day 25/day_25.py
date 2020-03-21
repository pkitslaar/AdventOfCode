import sys
from pathlib import Path
d5_dir = Path(__file__).parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))
from day_05 import run, txt_values

import heapq

with open(Path(__file__).parent / 'input.txt', 'r') as f:
    main_program = txt_values(f.read())

DROID_MANUAL, DROID_AUTO = range(2)

command_to_offset = {
            'north': ( 0, 1),
            'south': ( 0,-1),
            'west' : (-1, 0),
            'east' : ( 1, 0),
        }
offset_to_command = {v:k for k,v in command_to_offset.items()}

direction_to_opposite = {
    'north': 'south',
    'south': 'north',
    'east': 'west',
    'west': 'east',
}

class Strategy:

    def switch_to(self, NewStrategy):
        print(f'Switching to {NewStrategy}')
        self.__class__ = NewStrategy
        self.__init__()
        return self

class ExploreStrategy(Strategy):

    def __init__(self):
        self.ignore_items = {'infinite loop', 
                            'escape pod', 
                            'giant electromagnet',
                            'molten lava',
                            'photons',
                            }


    def next_command(self, droid, state):
            command = None
            valid_items = set(state['items']) - self.ignore_items
            if valid_items:
                item_to_pickup = list(valid_items)[0]
                command = f'take {item_to_pickup}'
            else:    
                if state['non_visited_doors']:
                    command = state['non_visited_doors'][0]
                else:
                    print('no more doors to visit backtracking')
                    if len(droid.route) > 1:
                        prev_room = droid.route[-2]
                        direction = droid.get_direction_for_node(droid.current_node, prev_room)
                        #step_to_prev_room = prev_room[0]-droid.current_pos[0], prev_room[1]-droid.current_pos[1]
                        #command = offset_to_command[step_to_prev_room]
                        #print('step to take', step_to_prev_room, 'command', command)
                        command = direction
                        del droid.route[-1]
                    else:
                        print('Visited all rooms')
                        self.switch_to(GoToSecurity)
                        return self.next_command(droid, state)
            return command

class GoToSecurity(Strategy):

    def next_command(self, droid, state):
        security_room = 'Security'
        if droid.current_node == security_room:
            print('Reached security room')
            self.switch_to(CrackPressureLock)
            return self.next_command(droid, state)
        else:
            arrival = droid.propagate(security_room)
            #print(arrival)
            current_arrival = arrival[droid.current_node]
            neighbor_arrival = [(arrival[n],n) for n in droid.get_connected_nodes(droid.current_node)]            
            neighbor_arrival.sort()
            next_room = neighbor_arrival[0][1]
            return droid.get_direction_for_node(droid.current_node, next_room)

        return None

import itertools

class CrackPressureLock(Strategy):

    def __init__(self):
        self.initialized = False
        self.permutations_to_check = None
        self.items_to_status = {}

    def initialize(self, droid):
        current_items_set = tuple(sorted(droid.inventory))
        self.permutations_to_check = {current_items_set}
        for n in range(1,len(current_items_set)+1):
            for comb in itertools.permutations(current_items_set, n):
                self.permutations_to_check.add(tuple(sorted(comb)))
        self.permutations_to_check = list(self.permutations_to_check)
        self.permutations_to_check.sort(key = lambda t: (len(t), t))
        for p in self.permutations_to_check:
            print(p)
        #raise
        #print(self.permutations_to_check)

    def next_command(self, droid, state):
        if not self.initialized:
            print('Initializing item permuations')
            self.initialize(droid)    
            self.initialized = True

        if droid.current_node != 'Security':
            print("No longer at security!!!!!!")
            return None

        #print(state)
        current_items_set = tuple(sorted(droid.inventory))
        if state.get('analysis_result'):
            print(current_items_set, state['analysis_result'][0])
            self.items_to_status[current_items_set] = state
            print('Checked', len(self.items_to_status), 'combination')
        
        while self.permutations_to_check and self.permutations_to_check[-1] in self.items_to_status:
            self.permutations_to_check.pop()
        if self.permutations_to_check:
            perm_to_check = set(self.permutations_to_check[-1])
            print('Checking perm', perm_to_check)
            current_set = set(current_items_set)
            print('Current set', current_set)
            missing_items = perm_to_check - current_set
            if missing_items:
                return 'take ' + str(list(missing_items)[0])
            redundant_items = current_set - perm_to_check
            if redundant_items:
                return 'drop ' + str(list(redundant_items)[0])
            
            # seems we have the items we want let check at the security
            return "south" 
        else:
            print('No more permutations')
            for comb, status in self.items_to_status.items():
                print(comb, status['analysis_result'][0])

class Droid():

    def __init__(self, mode=DROID_MANUAL):
        self.receive_buffer = []
        self.received_txt = None
        self.send_buffer = []

        
        self.current_node = None
        
        self.prev_node = None
        self.prev_command = None

        self.route = []
        self.nodes = {}
        self.edges_for_node = {}
        self.mode = mode
        self.inventory = []
        self.stategy = ExploreStrategy()

    #def get_room_pos(self, room_name):
    #    for pos, info in self.map.items():
    #        if info['room'] == room_name:
    #            return pos
    #    return None

    def set_node_for_direction(self, from_node, direction, to_node):
        self.edges_for_node.setdefault(from_node, {})[direction] = to_node
        op_direction = direction_to_opposite[direction]
        self.edges_for_node.setdefault(to_node, {})[op_direction] = from_node

    def get_node_in_direction(self, node, direction):
        edges = self.edges_for_node.get(node, {})
        return edges.get(direction)

    def get_connected_nodes(self, node):
        return list(self.edges_for_node.get(node, {}).values())

    def get_direction_for_node(self, from_node, to_node):
        edges = self.edges_for_node[from_node]
        for d, node in edges.items():
            if node == to_node:
                return d

    def propagate(self, start_node):
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
        items = []
        for l in lines:
            if l.startswith('- '):
                items.append(l[2:].strip())
            else:
                break
        return items

    def parse_lines(self, splitted_lines):
        parsed = {}
        if splitted_lines[0].startswith('=='):
            parsed['room'] = splitted_lines[0].split()[1]
            parsed['description'] = splitted_lines[1].strip()
            start_doors = splitted_lines.index('Doors here lead:')
            parsed['doors'] = self.parse_list(splitted_lines[start_doors+1:])
            try:
                start_items = splitted_lines.index('Items here:')
                parsed['items'] = self.parse_list(splitted_lines[start_items+1:])
            except ValueError:
                parsed['items'] = []
            if parsed['description'] == 'Analyzing...':
                start_analysis = start_doors+1+len(parsed['doors'])
                analysis_result = splitted_lines[start_analysis]
                parsed['analysis_result'] = (analysis_result, splitted_lines[start_analysis+1:])
        else:
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

    #def add_pos(self, current, offset):
    #    return (current[0]+offset[0], current[1]+offset[1])


    def next_command(self):
        print("-"*40)
        #if self.route and self.current_node != self.route[-1]:
        #    self.route.append(self.current_node)
        
        try:
            #print(self.received_txt)
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
                command = 'inv'
                self.nodes[self.current_node]['items'].append(dropped_item)
                #self.inventory.remove(dropped_item)
            elif status.startswith("You take the"):
                picked_up_item = status[12:-1].strip()
                command = 'inv'
                self.nodes[self.current_node]['items'].remove(picked_up_item)
                #self.inventory.append(picked_up_item)
                #print(self.inventory)

            if 'room' in parsed:                
                self.current_node = parsed['room']
                self.nodes[self.current_node] = parsed                
                if self.prev_command in direction_to_opposite:
                    self.set_node_for_direction(self.prev_node, self.prev_command, self.current_node)
                if not self.route or self.current_node != self.route[-1]:
                    self.route.append(self.current_node)                                        
            if 'ejected_room' in parsed:
                print("*** EJECTED BACK ***")
                self.current_node = self.route[-2]
                del self.route[-1]
                #print(self.map[self.current_pos])
        except Exception:
            print(self.received_txt)
            raise

        # Find next location to explore
        current_info = self.nodes[self.current_node]
        doors_in_room = current_info['doors']
        non_visited_doors = []
        for d in doors_in_room:            
            if not self.get_node_in_direction(self.current_node, d):
                non_visited_doors.append(d)
            #print(d, '*' if d_pos in self.map else '!')
        
        
        if self.mode == DROID_MANUAL:
            next_command_valid = False
            while not next_command_valid:
                command = input()
                if command.startswith(('take', 'drop', 'inv')) or command in doors_in_room:
                    next_command_valid = True
                else:
                    print('invalid command', command)
        else:
            if not command:
                state = {
                    'non_visited_doors': non_visited_doors,
                }
                state.update(current_info)
                if 'analysis_result' in parsed:
                    state['analysis_result'] = parsed['analysis_result']
                command = self.stategy.next_command(self, state)
                

        
        print(self.current_node, 'next command', command)
        #if command in command_to_offset:
        #    next_offset = command_to_offset[command]
        #    self.current_pos = self.add_pos(self.current_pos, next_offset)
        #    if not self.route or len(self.route) < 2 or self.current_pos != self.route[-2]:
        #        self.route.append(self.current_pos)
        #    else:
        #        if len(self.route) > 1:
        #            if self.current_pos == self.route[-2]:
        #                self.route = self.route[:-1]
        #    print(self.route)
        self.prev_command = command
        self.prev_node = self.current_node
        self.send_buffer = list(reversed([ord(c) for c in command] + [10]))

    def update_receive_txt(self):
        if self.receive_buffer:
            self.received_txt = ''.join(chr(v) for v in self.receive_buffer)
            self.receive_buffer = []

    def send(self):
        if self.receive_buffer:
            self.update_receive_txt()
            self.next_command()
        if self.send_buffer:
            v = self.send_buffer.pop()
            return v

    def receive(self, v):
        #print('received', v)
        self.receive_buffer.append(v)

if __name__ == "__main__":
    #d = Droid(DROID_MANUAL)
    d = Droid(DROID_AUTO)
    try:
        run(main_program, input_v=d.send, output_cb=d.receive, stop_on_output=False)
        d.update_receive_txt()
        print(d.received_txt)
    finally:
        #for pos, parsed in d.map.items():
        #    print(pos, parsed)
        pass
    #print(output)