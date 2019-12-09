import timeit
import itertools
import threading

from queue import Queue

PUZZLE_INPUT_PATH = "../input.txt"
PHASE_SETTINGS = [5,6,7,8,9]

class OpCode():
    def __init__(self, number, parameter_count):
        self.number = number
        self.parameter_count = parameter_count
                
    def __eq__(self, other):
        return self.number == other.number

op_codes = {
    '01': OpCode(1,  3),
    '02': OpCode(2,  3),
    '03': OpCode(3,  1),
    '04': OpCode(4,  1),
    '05': OpCode(5,  2),
    '06': OpCode(6,  2),
    '07': OpCode(7,  3),
    '08': OpCode(8,  3),
    '09': OpCode(9,  1),
    '99': OpCode(99, 0),
}

class Intcode():
    def __init__(self, name="", relative_base=0):
        self.name = name

        self.instruction_pointer = 0
        self.program = []
        self.running = False

        self.input = None
        self.output = None
        self.relative_base = relative_base 

    def load_program(self, program):
        self.memory = program
        self.program = program

    def execute(self):
        self.memory = self.program.copy()
        self.instruction_pointer = 0

        self.output = Queue(1)
        self.input = Queue(1)

        self.running = True

        while self.running:
            instruction = self.get_current_address()
            op_code, parameters = self.parse_op_code(instruction)

            if op_code == op_codes['01']:
                self.op_code_1(parameters)

            elif op_code == op_codes['02']:
                self.op_code_2(parameters)

            elif op_code == op_codes['03']:
                self.op_code_3(parameters)

            elif op_code == op_codes['04']:
                self.op_code_4(parameters)

            elif op_code == op_codes['05']:
                self.op_code_5(parameters)
                continue

            elif op_code == op_codes['06']:
                self.op_code_6(parameters)
                continue

            elif op_code == op_codes['07']:
                self.op_code_7(parameters)

            elif op_code == op_codes['08']:
                self.op_code_8(parameters)

            elif op_code == op_codes['09']:
                self.op_code_9(parameters)

            elif op_code == op_codes['99']:
                self.op_code_99()
                continue

            else:
                print("unknown operation: {}".format(op_code.number))

            _ = self.get_next_address()
        return self.get_memory(0)

    def parse_op_code(self, instruction):
        instruction = str(instruction)
        op_code = None
        param_modes = ""

        if len(instruction) < 2:
            op_code_key = "0" + instruction[-1:]
            op_code = op_codes[op_code_key]
        else:
            op_code_key = instruction[-2:]
            op_code = op_codes[op_code_key]
            param_modes = instruction[0:-2]

        # Fill in all parameters that did not have a mode defined.
        missing_param_count = op_code.parameter_count - len(param_modes)

        for _ in range(missing_param_count):
            param_modes = "0"+param_modes

        return (op_code, [{'mode': int(m)} for m in param_modes[::-1]])
    
    def get_next_param(self, mode, is_output=False):
        addr = self.get_next_address()

        if is_output:
            if mode == 2:
                return addr + self.relative_base
            else:
                return addr

        if mode == 0:
            return self.get_memory(addr)
        elif mode == 1:
            return addr
        elif mode == 2:
            return self.get_memory(addr + self.relative_base)
        else:
            print("unknown mode: {}".format(mode))

        return None

    def set_memory(self, address, value):
        try:
            self.memory[address] = value
        except IndexError:
            self.allocate_extra_mem(address)
            self.memory[address] = value

    def get_memory(self, address):
        try:
            val = self.memory[address]
        except IndexError:
            self.allocate_extra_mem(address)
            val = self.memory[address]
        
        return val

    def allocate_extra_mem(self, address):
        new_mem = [0]*(address - (len(self.memory)-1))
        self.memory.extend(new_mem)

    def get_next_address(self):
        self.instruction_pointer += 1
        return self.get_memory(self.instruction_pointer)

    def get_current_address(self):
        return self.get_memory(self.instruction_pointer)
    
    def set_instruction_pointer(self, address):
        self.instruction_pointer = address

    def op_code_1(self, parameters):
        """ Adds the values together and stores the result in address"""
        val1 = self.get_next_param(parameters[0]['mode'])
        val2 = self.get_next_param(parameters[1]['mode'])
        address = self.get_next_param(parameters[2]['mode'], True)
    
        self.set_memory(address, val1 + val2)

    def op_code_2(self, parameters):
        """ Multiplies the values and stores the result in address"""
        val1 = self.get_next_param(parameters[0]['mode'])
        val2 = self.get_next_param(parameters[1]['mode'])
        address = self.get_next_param(parameters[2]['mode'], True)
    
        self.set_memory(address, val1 * val2)
        
    def op_code_3(self, parameters):
        """ writes a value to the address"""
        val = self.input.get()
        address = self.get_next_param(parameters[0]['mode'], True)

        self.set_memory(address, val)
        
    def op_code_4(self, parameters):
        """ returns the value"""
        val1 = self.get_next_param(parameters[0]['mode'])

        self.output.put(val1)

    def op_code_5(self, parameters):
        """ Moves the instruction pointer to value2 if value one is non-zero"""
        val1 = self.get_next_param(parameters[0]['mode'])
        val2 = self.get_next_param(parameters[1]['mode'])

        if (val1 != 0):
            self.set_instruction_pointer(val2)
        else:
            self.get_next_address()

    def op_code_6(self, parameters):
        """ Moves the instruction pointer to value2 if value one is zero"""
        val1 = self.get_next_param(parameters[0]['mode'])
        val2 = self.get_next_param(parameters[1]['mode'])
    
        if (val1 == 0):
            self.set_instruction_pointer(val2)
        else:
            self.get_next_address()

    def op_code_7(self, parameters):
        """ Sets address to 1 if value1 is smaller then value2. the address gets set to 0 otherwise"""
        val1 = self.get_next_param(parameters[0]['mode'])
        val2 = self.get_next_param(parameters[1]['mode'])
        address = self.get_next_param(parameters[2]['mode'], True)

        value = 0

        if (val1 < val2):
            value = 1
        self.set_memory(address, value)

    def op_code_8(self, parameters):
        """ Sets address to 1 if value1 is equal to value2. the address gets set to 0 otherwise"""
        val1 = self.get_next_param(parameters[0]['mode'])
        val2 = self.get_next_param(parameters[1]['mode'])
        address = self.get_next_param(parameters[2]['mode'], True)

        value = 0

        if (val1 == val2):
            value = 1
    
        self.set_memory(address, value)

    def op_code_9(self, parameters):
        """ Sets the relative base to value1"""
        val1 = self.get_next_param(parameters[0]['mode'])

        self.relative_base = self.relative_base + val1

    def op_code_99(self):
        self.running = False


def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    inputs = []
    with open(PUZZLE_INPUT_PATH) as f:
        inputs = [int(intval) for intval in f.readline().split(",")]
    
    return inputs

def solve():
    program = read_puzzle_input()

    boost = Intcode("BOOST")
    boost.load_program(program)

    execute = threading.Thread(target=boost.execute)
    execute.start()

    boost.input.put(2)
    while execute.is_alive() or not boost.output.empty():
        print(boost.output.get())



if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))