from main import Intcode

def test_parse_op_code():
    print('------------ test_parse_op_code ------------ ')

    tests = [
        {
            'instruction': '1002',
            'expected_modes': '010',
            'expected_op_code_num': 2,
        },
        {
            'instruction': '1102',
            'expected_modes': '011',
            'expected_op_code_num': 2,
        },
        {
            'instruction': '11102',
            'expected_modes': '111',
            'expected_op_code_num': 2,
        },
        {
            'instruction': '02',
            'expected_modes': '000',
            'expected_op_code_num': 2,
        },
        {
            'instruction': '2',
            'expected_modes': '000',
            'expected_op_code_num': 2,
        },
        {
            'instruction': '99',
            'expected_modes': '',
            'expected_op_code_num': 99,
        },
        {
            'instruction': '01',
            'expected_modes': '000',
            'expected_op_code_num': 1,
        },
        {
            'instruction': '03',
            'expected_modes':'0' ,
            'expected_op_code_num': 3,
        },
        {
            'instruction': '103',
            'expected_modes':'1' ,
            'expected_op_code_num': 3,
        },
    ]

    for i, t in enumerate(tests):
        computer = Intcode()
        op_code, modes = computer.parse_op_code(t['instruction'])
        if(op_code.number != t['expected_op_code_num']):
            print("{}: {} != {}".format(i, op_code.number, t['expected_op_code_num']))
        if (modes != t['expected_modes']):
            print("{}: {} != {}".format(i, modes, t['expected_modes']))

def test_execute():
    print('------------ test_execute ------------ ')
    tests = [
        {
            'program': [1002,4,3,4,33],
            'output': 1002,
        },
        {
            'program': [1,0,0,0,99],
            'output': 2,
        },
        {
            'program': [1,1,1,4,99,5,6,0,99],
            'output': 30,
        },
        {
            'program': [3,1,99],
            'output': 3,
        },
        {
            'program': [3,0,99],
            'output': 1,
        },
        {
            'program': [1101,225,6,6,99,0,0,0],
            'output': 1101,
        },
    ]

    for i, t in enumerate(tests):
        computer = Intcode()
        computer.load_program(t['program'])
        result = computer.execute()

        if (result != t['output']):
            print("{}: {} != {}".format(i, result, t['output']))


if __name__ == "__main__":
    test_parse_op_code()
    test_execute()
    pass