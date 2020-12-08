class CPU:
    def __init__(self, program_txt):
        self._program = [l.strip() for l in program_txt.splitlines()]

        self._accumulator = 0
        self._program_counter = 0
    
    def step(self):
        instruction, *args = self._program[self._program_counter].split()
        getattr(self, instruction)(*args) # run instruction
        return {'pc': self._program_counter, 'a': self._accumulator}

    def acc(self, value):
        self._accumulator += int(value)
        self._program_counter += 1
    
    def jmp(self, value):
        self._program_counter += int(value)
    
    def nop(self, _):
        self._program_counter += 1

    
