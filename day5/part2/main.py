
PUZZLE_INPUT_PATH = "../input.txt"

class OpCode():
    def __init__(self, number, default_params):
        self.number = number
        self.param_count = len(default_params)
        self.default_params = default_params
        
    def __eq__(self, other):
        return self.number == other.number

op_codes = {
    '01': OpCode(1,  '100'),
    '02': OpCode(2,  '100'),
    '03': OpCode(3,  '1'),
    '04': OpCode(4,  '0'),
    '05': OpCode(5,  '00'),
    '06': OpCode(6,  '00'),
    '07': OpCode(7,  '100'),
    '08': OpCode(8,  '100'),
    '99': OpCode(99, ''),
}

class Intcode():
    def __init__(self):
        self.instruction_pointer = 0
        self.program = []
        self.running = False

        self.opcode3_inputs = []
        self.opcode4_outputs = []

    def load_program(self, program):
        self.memory = program
        self.program = program

    def execute(self):
        self.memory = self.program.copy()
        self.instruction_pointer = 0
        self.running = True

        while self.running:
            instruction = self.get_address_value()
            op_code, param_modes = self.parse_op_code(instruction)
            params = self.parse_parameters_for_op_code(op_code, param_modes)

            if op_code == op_codes['01']:
                self.op_code_1(params[0], params[1], params[2])
            elif op_code == op_codes['02']:
                self.op_code_2(params[0], params[1], params[2])
            elif op_code == op_codes['03']:
                self.op_code_3(params[0])
            elif op_code == op_codes['04']:
                self.op_code_4(params[0])
            elif op_code == op_codes['05']:
                self.op_code_5(params[0], params[1])
                continue
            elif op_code == op_codes['06']:
                self.op_code_6(params[0], params[1])
                continue
            elif op_code == op_codes['07']:
                self.op_code_7(params[0], params[1], params[2])
            elif op_code == op_codes['08']:
                self.op_code_8(params[0], params[1], params[2])
            elif op_code == op_codes['99']:
                self.op_code_99()
                continue
            else:
                print("unknown operation: {}".format(op_code.number))

            _ = self.get_next_address_value()

        return self.get_memory(0)

    def get_output(self):
        if len(self.opcode4_outputs) > 0:
            return self.opcode4_outputs[-1]
        return None

    def set_inputs(self, inputs):
        self.opcode3_inputs = inputs

    def parse_op_code(self, instruction):
        instruction = str(instruction)
        op_code = None
        override_param_modes = ""

        if len(instruction) < 2:
            op_code_key = "0" + instruction[-1:]
            op_code = op_codes[op_code_key]
        else:
            op_code_key = instruction[-2:]
            op_code = op_codes[op_code_key]
            override_param_modes = instruction[0:-2]

        param_modes = op_code.default_params

        # Fill in all parameters that did not have an mode defined.
        if len(override_param_modes) > 0:
            default_end_index = len(param_modes) - len(override_param_modes)
            param_modes = param_modes[:default_end_index] + override_param_modes

        return (op_code, param_modes)
    
    def parse_parameters_for_op_code(self, op_code, param_modes):
        parameters = []

        for mode in param_modes[::-1]:
            addr = self.get_next_address_value()

            if mode == '0':
                val = self.get_memory(addr)
                parameters.append(val)
            elif mode == '1':
                parameters.append(addr)
            else:
                print("unknown mode: {}".format(mode))

        return parameters

    def set_memory(self, address, value):
        self.memory[address] = value

    def get_memory(self, address):
        return self.memory[address]

    def get_next_address_value(self):
        self.instruction_pointer += 1
        return self.get_memory(self.instruction_pointer)

    def get_address_value(self):
        return self.get_memory(self.instruction_pointer)
    
    def set_instruction_pointer(self, address):
        self.instruction_pointer = address

    def op_code_1(self, value1, value2, address):
        """ Adds the values together and stores the result in address"""
        self.set_memory(address, value1 + value2)

    def op_code_2(self, value1, value2, address):
        """ Multiplies the values and stores the result in address"""
        self.set_memory(address, value1 * value2)
        
    def op_code_3(self, address):
        """ writes a value to the address"""
        self.set_memory(address, self.opcode3_inputs[0])
        
    def op_code_4(self, address):
        """ returns the value at the address"""
        self.opcode4_outputs.append(address)

    def op_code_5(self, value1, value2):
        """ Moves the instruction pointer to value2 if value one is non-zero"""
        if (value1 != 0):
            self.set_instruction_pointer(value2)
        else:
            self.get_next_address_value()

    def op_code_6(self, value1, value2):
        """ Moves the instruction pointer to value2 if value one is zero"""
        if (value1 == 0):
            self.set_instruction_pointer(value2)
        else:
            self.get_next_address_value()

    def op_code_7(self, value1, value2, address):
        """ Sets address to 1 if value1 is smaller then value2. the address gets set to 0 otherwise"""
        value = 0
        if (value1 < value2):
            value = 1
        self.set_memory(address, value)

    def op_code_8(self, value1, value2, address):
        """ Sets address to 1 if value1 is equal to value2. the address gets set to 0 otherwise"""
        value = 0
        if (value1 == value2):
            value = 1
        self.set_memory(address, value)

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

if __name__ == "__main__":
    program = read_puzzle_input()

    comp = Intcode()
    comp.set_inputs([5])
    comp.load_program(program)

    result = comp.execute()
    print(comp.get_output())
