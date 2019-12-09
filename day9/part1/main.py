import timeit
import itertools
import threading

from queue import Queue

PUZZLE_INPUT_PATH = "../input.txt"
PHASE_SETTINGS = [5,6,7,8,9]

class OpCode():
    def __init__(self, number, parameters):
        self.number = number
        self.parameters = parameters
                
    def __eq__(self, other):
        return self.number == other.number

    def get_parameter_options(self, modes):
        params = self.parameters.copy()
        for i, p in enumerate(params[::-1]):
            try:
                p.mode = int(modes[i])
            except IndexError:
                p.mode = 0
        return params

class Parameter():
    def __init__(self, is_output=False, mode=0):
        self.is_output = is_output
        self.mode = mode

op_codes = {
    '01': OpCode(1,  [Parameter(), Parameter(), Parameter(True)]),
    '02': OpCode(2,  [Parameter(), Parameter(), Parameter(True)]),
    '03': OpCode(3,  [Parameter(True)]),
    '04': OpCode(4,  [Parameter()]),
    '05': OpCode(5,  [Parameter(), Parameter()]),
    '06': OpCode(6,  [Parameter(), Parameter()]),
    '07': OpCode(7,  [Parameter(), Parameter(), Parameter(True)]),
    '08': OpCode(8,  [Parameter(), Parameter(), Parameter(True)]),
    '09': OpCode(9,  [Parameter()]),
    '99': OpCode(99, []),
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
            print(self.memory)
            instruction = self.get_current_address()
            op_code, parameters = self.parse_op_code(instruction)
            addresses = self.parse_addresses(parameters)

            if op_code == op_codes['01']:
                self.op_code_1(addresses[0], addresses[1], addresses[2])

            elif op_code == op_codes['02']:
                self.op_code_2(addresses[0], addresses[1], addresses[2])

            elif op_code == op_codes['03']:
                self.op_code_3(addresses[0])

            elif op_code == op_codes['04']:
                self.op_code_4(addresses[0])

            elif op_code == op_codes['05']:
                self.op_code_5(addresses[0], addresses[1])
                continue

            elif op_code == op_codes['06']:
                self.op_code_6(addresses[0], addresses[1])
                continue

            elif op_code == op_codes['07']:
                self.op_code_7(addresses[0], addresses[1], addresses[2])

            elif op_code == op_codes['08']:
                self.op_code_8(addresses[0], addresses[1], addresses[2])

            elif op_code == op_codes['09']:
                self.op_code_9(addresses[0])

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

        return (op_code, op_code.get_parameter_options(param_modes))
    
    def parse_addresses(self, parameters):
        addresses = []

        for param in parameters:
            addr = self.get_next_address()
            # print(addresses, addr, param.is_output, param.mode)

            if param.is_output:
                if param.mode == 0:
                    addresses.append(addr)
                elif param.mode == 1:
                    addresses.append(addr)
                elif param.mode == 2:
                    addresses.append(addr + self.relative_base)   
                else:
                    print("unknown mode: {}".format(param.mode))
                continue

            if param.mode == 0:
                addresses.append(self.get_memory(addr))
            elif param.mode == 1:
                addresses.append(addr)
            elif param.mode == 2:
                addresses.append(self.get_memory(addr + self.relative_base))
            else:
                print("unknown mode: {}".format(param.mode))

        return addresses

    def set_memory(self, address, value):
        try:
            self.memory[address] = value
        except IndexError:
            self.allocate_extra_mem(address)
            self.memory[address] = value

    def get_memory(self, address):
        try:
            val  = self.memory[address]
        except IndexError:
            self.allocate_extra_mem(address)
            val= self.memory[address]
        
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

    def op_code_1(self, value1, value2, address):
        """ Adds the values together and stores the result in address"""
        val1 = self.get_memory(value1)
        val2 = self.get_memory(value2)

        print(val1, val2, address)

        self.set_memory(address, val1 + val2)

    def op_code_2(self, value1, value2, address):
        """ Multiplies the values and stores the result in address"""
        val1 = self.get_memory(value1)
        val2 = self.get_memory(value2)
    
        self.set_memory(address, val1 * val2)
        
    def op_code_3(self, address):
        """ writes a value to the address"""
        val = self.input.get()
        self.set_memory(address, val)
        
    def op_code_4(self, value):
        """ returns the value"""
        self.output.put(value)

    def op_code_5(self, value1, value2):
        """ Moves the instruction pointer to value2 if value one is non-zero"""
        val1 = self.get_memory(value1)
        val2 = self.get_memory(value2)

        if (val1 != 0):
            self.set_instruction_pointer(val2)
        else:
            self.get_next_address()

    def op_code_6(self, value1, value2):
        """ Moves the instruction pointer to value2 if value one is zero"""
        val1 = self.get_memory(value1)
        val2 = self.get_memory(value2)
    
        if (val1 == 0):
            self.set_instruction_pointer(val2)
        else:
            self.get_next_address()

    def op_code_7(self, value1, value2, address):
        """ Sets address to 1 if value1 is smaller then value2. the address gets set to 0 otherwise"""
        val1 = self.get_memory(value1)
        val2 = self.get_memory(value2)
        value = 0

        if (val1 < val1):
            value = 1
        self.set_memory(address, value)

    def op_code_8(self, value1, value2, address):
        """ Sets address to 1 if value1 is equal to value2. the address gets set to 0 otherwise"""
        val1 = self.get_memory(value1)
        val2 = self.get_memory(value2)
        value = 0

        if (val1 == val2):
            value = 1
    
        self.set_memory(address, value)

    def op_code_9(self, value1):
        """ Sets the relative base to value1"""
        self.relative_base = self.relative_base + self.get_memory(value1)

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

    boost.input.put(1)
    while execute.is_alive() or not boost.output.empty():
        # _ = boost.output.get()
        print(boost.output.get())



if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))