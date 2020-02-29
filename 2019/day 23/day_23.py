import sys
from pathlib import Path
d5_dir = Path(__file__).parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))
from day_05 import run, txt_values


with open(Path(__file__).parent / 'input.txt', 'r') as f:
    main_program = txt_values(f.read())

import threading
import queue
import time

class StopComputation(Exception):
    pass

class Computer():

    def __init__(self, address, all_queues):
        self.address = address
        self.send_adress = False
        self.incoming_packets = all_queues[self.address]
        self.outgoing_packets = all_queues
        self.last_outgoing_packet = []
        self.last_incoming_packet = []
        self.all_received = []
        self.num_send = 0
        self.num_empty_queues = 0
        self.idle = False

    def log(self, *args):
        #print(self.address, *args)
        pass

    def run(self):
        try:
            run(main_program[:], input_v=self.receive, output_cb=self.send, stop_on_output=False)
        except StopComputation:
            pass

    def receive(self):
        if not self.send_adress:
            self.send_adress = True
            self.log('sending adress', self.address)
            return self.address
        else:
            if self.last_incoming_packet:
                packet_part = self.last_incoming_packet[0]
                del self.last_incoming_packet[0]
                self.log('receiving packet part', packet_part)
                return packet_part
            else:
                if self.incoming_packets.empty():
                    #print(self.address, 'no incoming packets')
                    self.idle = True
                    time.sleep(0.01)
                    return -1
                else:
                    self.idle = False
                    packet_value = self.incoming_packets.get()
                    if packet_value is None:
                        self.log('stopping')
                        raise StopComputation()
                    self.last_incoming_packet = list(packet_value)
                    self.all_received.append(packet_value)
                    self.log('received packet', self.last_incoming_packet)
                    return -1

    def send(self, value):
        self.log('send', value)
        self.last_outgoing_packet.append(value)
        if len(self.last_outgoing_packet) > 2:
            adress_to_send_to = int(self.last_outgoing_packet[0])
            self.log('adding packet to queue of adress', adress_to_send_to)
            self.outgoing_packets[adress_to_send_to].put(tuple(self.last_outgoing_packet[1:]))
            self.last_outgoing_packet = []

class Network():

    def __init__(self):

        self.computer_queues = {i:queue.Queue() for i in range(50)}
        self.computer_queues[255] = queue.Queue()
        self.all_computers = [Computer(i, self.computer_queues) for i in range(50)]
        self.threads = []
        for c in self.all_computers:
            t = threading.Thread(target=c.run)
            self.threads.append(t)
            t.start()

    def stop(self):   
        for i in range(50):
            q = self.computer_queues[i]
            q.put(None)
        for t in self.threads:
            t.join()

def part_1():
    n = Network()
    first_value = n.computer_queues[255].get()
    n.stop()
    print('Part 1', first_value[1])

def part_2():
    n = Network()
    last_nat_value = None
    send_to_zero = []
    while True:
            time.sleep(0.01)
            while not n.computer_queues[255].empty():
                last_nat_value = n.computer_queues[255].get()
            if last_nat_value:
                if all(n.all_computers[i].idle for i in range(50)):
                    #print('Idle sending', last_nat_value)
                    send_to_zero.append(last_nat_value)
                    n.computer_queues[0].put(last_nat_value)
                    last_nat_value = None
                    if len(send_to_zero) > 1:
                        if send_to_zero[-1][1] == send_to_zero[-2][1]:
                            print('Part 2', send_to_zero[-1][1])
                            n.stop()
                            return





if __name__ == "__main__":
    part_1()
    part_2()

