"""
Advent of Code 2024 - Day 17
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

class CPU():
    def __init__(self, A, B, C, program_counter=0):
        self.registers = {'A': A, 'B': B, 'C': C,}
        self.combo_operand_names = {
            4: 'A',
            5: 'B',
            6: 'C',
        }
        self.op_codes = [
           self.op_adv,
           self.op_bxl,
           self.op_bst,
           self.op_jnz,
           self.op_bxc,
           self.op_out,
           self.op_bdv,
           self.op_cdv,
        ]
        self.program_counter = program_counter
        self.output = []
    
    def combo_operand(self, operand):
        if operand < 4:
            return operand
        return self.registers[self.combo_operand_names[operand]]

    def op_adv(self, operand):
        """
        The adv instruction (opcode 0) performs division. 
        The numerator is the value in the A register. 
        The denominator is found by raising 2 to the power of the instruction's combo operand
        The result of the division operation is truncated to an integer and then written to the A register
        """
        numerator = self.registers['A']
        denominator = 2**self.combo_operand(operand)
        self.registers['A'] = numerator // denominator
        self.program_counter += 2

    def op_bxl(self, operand):
        """"
        The bxl instruction (opcode 1) calculates the bitwise XOR 
        of register B and the instruction's literal operand, 
        then stores the result in register B.
        """
        self.registers['B'] = self.registers['B'] ^ operand
        self.program_counter += 2

    def op_bst(self, operand):
        """
        The bst instruction (opcode 2) calculates the value of its 
        combo operand modulo 8 (thereby keeping only its lowest 3 bits), 
        then writes that value to the B register.
        """
        self.registers['B'] = self.combo_operand(operand) % 8
        self.program_counter += 2

    def op_jnz(self, operand):
        """
        The jnz instruction (opcode 3) 
        does nothing if the A register is 0. 
        However, if the A register is not zero, 
        it jumps by setting the instruction pointer 
        to the value of its literal operand; 
        if this instruction jumps, 
        the instruction pointer is not increased by 2 after this 
        instruction.
        """
        assert operand < 4
        if self.registers['A'] != 0:
            self.program_counter = operand
        else:
            self.program_counter += 2   

    def op_bxc(self, operand):
        """
        The bxc instruction (opcode 4) calculates 
        the bitwise XOR of register B and register C, 
        then stores the result in register B. 
        (For legacy reasons, this instruction reads an 
        operand but ignores it.)
        """
        self.registers['B'] = self.registers['B'] ^ self.registers['C']
        self.program_counter += 2

    def op_out(self, operand):
        """
        The out instruction (opcode 5) calculates 
        the value of its combo operand modulo 8, 
        then outputs that value. 
        (If a program outputs multiple values, they are separated by commas.)
        """
        value = self.combo_operand(operand) % 8
        self.output.append(value)
        self.program_counter += 2

    def op_bdv(self, operand):
        """
        The bdv instruction (opcode 6) works exactly 
        like the adv instruction except that the result 
        is stored in the B register. 
        (The numerator is still read from the A register.)
        """
        numerator = self.registers['A']
        denominator = 2**self.combo_operand(operand)
        self.registers['B'] = numerator // denominator
        self.program_counter += 2
    
    def op_cdv(self, operand):
        """
        The cdv instruction (opcode 7) works exactly 
        like the adv instruction except that the result 
        is stored in the C register. 
        (The numerator is still read from the A register.)
        """
        numerator = self.registers['A']
        denominator = 2**self.combo_operand(operand)
        self.registers['C'] = numerator // denominator
        self.program_counter += 2
    
    def run(self, program):
        while self.program_counter < len(program):
            op_code = program[self.program_counter]
            operand = program[self.program_counter+1]
            self.op_codes[op_code](operand)


def parse(data):
    lines = data.strip().splitlines()
    registers = {}
    program = []
    for line in lines:
        if not line.strip():
            continue
        if len(registers) < 3:
            register, value = line.split(' ',1)[1].split(':')
            registers[register] = int(value)
        else:
            program = [int(x) for x in line.split(': ',1)[1].split(',')]
    return registers, program
            

def solve(data, part2=False):
    registers, program = parse(data)
    if not part2:
        cpu = CPU(**registers)
        cpu.run(program)
        return ",".join(map(str, cpu.output))



def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == "4,6,3,5,6,3,5,2,1,0"


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result != '1,1,4,4,3,3,7,7,0' # issue with literal and combo operands
    assert result == '2,3,6,2,1,6,1,2,1'

EXAMPLE_DATA2 = """\
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

def test_example2():
    # quick test to see if the program produces a copy
    register, program = parse(EXAMPLE_DATA2)
    result = solve(EXAMPLE_DATA2, part2=False)
    assert result == ",".join(map(str, program))


def test_part2():
    """
    Program: 2,4, 1,6, 7,5, 4,6, 1,4, 5,5, 0,3, 3,0

    2,4 -> B = A % 8
    1,6 -> B = B ^ 6
    7,5 -> C = A // 2**B
    4,6 -> B = B ^ C
    1,4 -> B = B ^ 4
    5,5 -> output B % 8
    0,3 -> A = A // 2**3
    3,0 -> jump to 0 if A != 0

    The program does the follwoing
     - take the last 3 bits of A as B
     - xor B with 6
     - take the next set of 3 bits from A starting from B-th as C

    """
    _, program = parse(data())


    A_parts = ['0']*16
    for i in range(16):
        for j in range(8):
            A_parts[i] = str(j)
            A = int(''.join(A_parts),8)
            cpu = CPU(A, 0, 0)
            cpu.run(program)
            result = cpu.output
            if result[:i] == program[:i]:
                break
        

    

    cpu = CPU(int('7'*3,8), 0, 0)
    cpu.run(program)
    result = cpu.output


        

    print("Part 2:", result)
    assert result == -1


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()