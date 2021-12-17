"""
Advent of Code 2021 - Day 16
Pieter Kitslaar
"""

import operator
from pathlib import Path

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def type_literal(bits):
    value_bits = []
    for start in range(0,len(bits),5):
        value_bits.append(bits[start+1:start+5])
        if bits[start] =='0':
            break   
    return 5*len(value_bits), int(''.join(value_bits),2)

def type_operator(bits):
    length_type = int(bits[0],2)
    sub_packet_info = {}
    if length_type==0:
        total_length_bits = bits[1:16]
        total_sub_packets_length = int(total_length_bits,2)
        sub_packet_info['total_length'] = total_sub_packets_length
        sub_packet_info['data'] = bits[16:16+total_sub_packets_length]
        sub_packet_info['offset'] = 16

    else:
        num_sub_packets = int(bits[1:12],2)
        sub_packet_info['num_packets'] = num_sub_packets
        sub_packet_info['data'] = bits[12:]
        sub_packet_info['offset'] = 12
    return sub_packet_info


def parse(hex_txt):
    bits = ''.join(f'{int(c,16):04b}' for c in hex_txt.strip())
    return parse_bits(bits)

def nearest_multiple(v, n):
    return n*int((v/n)+0.5)

def test_nearst_mupltiple():
    8 == nearest_multiple(8,8)
    24 == nearest_multiple(23,8)
    16 == nearest_multiple(15,8)
    24 == nearest_multiple(17,8)
    24 == nearest_multiple(21,4)
    36 == nearest_multiple(33,4)

def parse_bits(bits, sub_level=0):
    version = int(bits[:3],2)
    packet_id = int(bits[3:6],2)
    if packet_id == 4:
        num_literal_bits_parsed, literal_value = type_literal(bits[6:])
        return (6+num_literal_bits_parsed, version, packet_id, literal_value)
    else:
        sub_info = type_operator(bits[6:])
        if not sub_info:
            return (len(bits), 0, -1, -1)
        else:
            sub_data = sub_info['data']
            sub_packets = []
            current_total_length = 0
            while True:
                sub_p = parse_bits(sub_data, sub_level=sub_level+1)
                #print(' '*sub_level, sub_p, sub_data)
                sub_packets.append(sub_p)
                if 'num_packets' in sub_info:
                    current_total_length += sub_p[0]
                    if len(sub_packets) == sub_info['num_packets']:
                        #current_total_length = len(bits)
                        break
                else:
                    current_total_length += sub_p[0]
                    if current_total_length >= sub_info['total_length']:
                        #print(current_total_length)
                        break
                sub_data = sub_info['data'][current_total_length:]
                
            return (6+sub_info['offset']+current_total_length, version, packet_id, sub_packets)

def solve1(txt):
    p = parse(txt)
    version_sum = 0
    packages = [p]
    while packages:
        new_packages = []
        for p in packages:
            version_sum+=p[1]
            if p[2] != 4 and p[2] > -1:
                new_packages.extend(p[3])
        packages = new_packages
    return version_sum

def test_example1():

    p = parse('D2FE28')
    print(p)
    assert (21, 6,4, 2021) == p

    p = parse('38006F45291200')
    print(p)
    assert (49, 1, 6) == p[:3]
    assert 2 == len(p[3])
    assert (11, 6, 4, 10) == p[3][0]
    assert (16, 2, 4, 20) == p[3][1]

    p = parse('EE00D40C823060')
    print(p)
    assert (51, 7, 3) == p[:3]
    assert 3 == len(p[3])
    assert (11,2,4,1) == p[3][0]
    assert (11,4,4,2) == p[3][1]
    assert (11,1,4,3) == p[3][2]

    result = solve1('8A004A801A8002F478')
    assert 16 == result
    #print(parse('8A004A801A8002F478'))

    #print(parse('A0016C880162017C3686B18A3D4780'))
    31 == solve1('A0016C880162017C3686B18A3D4780')
    12 == solve1('620080001611562C8802118E34')
    23 == solve1('C0015000016115A2E0802F182340')

def test_part1():
    result = solve1(get_input())
    print('Part 1', result)

def compute(packet):
    p_id = packet[2]
    if p_id == 4:
        return packet[3]
    else:
        values = [compute(p) for p in packet[3]]
        if p_id == 0:
            # sum
            return sum(values)
        elif p_id == 1:
            # product
            result = 1
            for v in values:
                result = result*v
            return result
        elif p_id == 2:
            # min
            return min(values)
        elif p_id == 3:
            # max
            return max(values)
        elif p_id == 5:
            # greater
            assert 2== len(values)
            return int(values[0] > values[1])
        elif p_id == 6:
            # less than
            assert 2== len(values)
            return int(values[0] < values[1])
        elif p_id == 7:
            # equal
            assert 2== len(values)
            return int(values[0] == values[1])
        else:
            raise ValueError('Unknown Packet ID', p_id)

def solve2(txt):
    return compute(parse(txt))

def test_example2():
    3 == solve2('C200B40A82')
    54 == solve2('04005AC33890')
    7 == solve2('880086C3E88112')
    9 == solve2('CE00C43D881120')
    1 == solve2('D8005AC2A8F0')
    0 == solve2('F600BC2D8F')
    0 == solve2('9C005AC2F8F0')
    1 == solve2('9C0141080250320F1802104A08')

def test_part2():
    result = solve2(get_input())
    print('Part 2', result)

if __name__ == "__main__":
    test_nearst_mupltiple()
    test_example1()
    test_part1()
    test_example2()
    test_part2()