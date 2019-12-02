
PUZZLE_INPUT_PATH = "../input.txt"

def run_program(program):
    """ Runs the given program.

    :param program: A list of ints, which reprensets the program.
    :returns: The output of the program.
    """
    halt = False
    reader_index = 0
    running_program = program

    while not halt:
        op_code = running_program[reader_index]

        if op_code == 99:
            halt = True
            break

        op = operations[op_code]
        running_program, reader_index = op(running_program, reader_index)

    return running_program[0]


def opcode_one(program, reader_index):
    input_val_1, input_val_2 = get_input_values(program, reader_index)
    output_val = input_val_1 + input_val_2

    program = write_output_value(program, reader_index, output_val)
    reader_index +=4

    return (program, reader_index)

def opcode_two(program, reader_index):
    input_val_1, input_val_2 = get_input_values(program, reader_index)
    output_val = input_val_1 * input_val_2

    program = write_output_value(program, reader_index, output_val)
    reader_index +=4

    return (program, reader_index)

operations = {
    1: opcode_one,
    2: opcode_two,
}

def get_input_values(program, reader_index):
    input_postition_1 = program[reader_index+1]
    input_postition_2 = program[reader_index+2]

    input_val_1 = program[input_postition_1]
    input_val_2 = program[input_postition_2]

    return (input_val_1, input_val_2)

def write_output_value(program, reader_index, value):
    output_postition = program[reader_index+3]
    program[output_postition] = value


    return program


def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    inputs = []
    with open(PUZZLE_INPUT_PATH) as f:
        inputs = [int(intval) for intval in f.readline().split(",")]
    
    return inputs

if __name__ == "__main__":
    intlist = read_puzzle_input()

    
    intlist[1] = 12
    intlist[2] = 2

    result = run_program(intlist)
    print(result)

