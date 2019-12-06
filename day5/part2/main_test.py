from main import Intcode


def test_execute():
    print('------------ test_execute ------------ ')
    tests = [
        {
            'program': [1107,50,60,7,4,7,99,0],
            'input': 0,
            'output': 1,
        },
        {
            'program': [1107,50,10,7,4,7,99,0],
            'input': 0,
            'output': 0,
        },
        {
            'program': [7,8,9,7,4,7,99,0,50,60],
            'input': 0,
            'output': 1,
        },
        {
            'program': [7,8,9,7,4,7,99,0,50,10],
            'input': 0,
            'output': 0,
        },
        {
            'program': [1108,50,60,7,4,7,99,0],
            'input': 0,
            'output': 0,
        },
        {
            'program': [1108,50,50,7,4,7,99,0],
            'input': 0,
            'output': 1,
        },
        {
            'program': [8,8,9,7,4,7,99,0,50,60],
            'input': 0,
            'output': 0,
        },
        {
            'program': [8,8,9,7,4,7,99,0,50,50],
            'input': 0,
            'output': 1,
        },
        {
            'program': [3,9,8,9,10,9,4,9,99,-1,8],
            'input': 8,
            'output': 1,
        },
        {
            'program': [3,9,8,9,10,9,4,9,99,-1,8],
            'input': 7,
            'output': 0,
        },
        {
            'program': [3,9,7,9,10,9,4,9,99,-1,8],
            'input': 1,
            'output': 1,
        },
        {
            'program': [3,9,7,9,10,9,4,9,99,-1,8],
            'input': 10,
            'output': 0,
        },
        {
            'program': [3,3,1108,-1,8,3,4,3,99],
            'input': 8,
            'output': 1,
        },
        {
            'program': [3,3,1108,-1,8,3,4,3,99],
            'input': 10,
            'output': 0,
        },
        {
            'program': [3,3,1107,-1,8,3,4,3,99],
            'input': 2,
            'output': 1,
        },
        {
            'program': [3,3,1107,-1,8,3,4,3,99],
            'input': 10,
            'output': 0,
        },
        {
            'program': [1105,1,6,0,0,0,99],
            'input': 0,
            'output': None,
        },
        {
            'program': [1106,0,6,0,0,0,99],
            'input': 0,
            'output': None,
        },
        {
            'program': [1106,0,6,0,0,0,1105,0,3,99],
            'input': 0,
            'output': None,
        },
        {
            'program': [1105,1,6,0,0,0,1106,1,3,99],
            'input': 0,
            'output': None,
        },
        {
            'program': [1105,1,6,0,0,0,1105,0,88,99],
            'input': 0,
            'output': None,
        },
        {
            'program': [1106,0,6,0,0,0,1106,1,88,4,0,99],
            'input': 0,
            'output': 1106,
        },
        {
            'program': [5,1,3,6,0,0,4,0,99],
            'input': 0,
            'output': 5,
        },
        {
            'program': [6,0,3,6,0,0,4,0,99],
            'input': 0,
            'output': 6,
        },
        {
            'program': [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],
            'input': 0,
            'output': 0,
        },
        {
            'program': [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],
            'input': 0,
            'output': 0,
        },
        {
            'program': [3,3,1105,-1,9,1101,0,0,12,4,12,99,1],
            'input': 1,
            'output': 1,
        },
        {
            'program': [3,3,1105,-1,9,1101,0,0,12,4,12,99,1],
            'input': 0,
            'output': 0,
        },
        {
            'program': [3,3,1105,-1,9,1101,0,0,12,4,12,99,1],
            'input': 9,
            'output': 1,
        },
        {
            'program': [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
            'input': 1,
            'output': 999,
        },
        {
            'program': [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
            'input': 8,
            'output': 1000,
        },
        {
            'program': [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
            'input': 19,
            'output': 1001,
        },
        {
            'program': [3,11,1,11,11,11,4,11,99,0,0,0],
            'input': 5,
            'output': 10,
        },
    ]

    for i, t in enumerate(tests):
        computer = Intcode()
        computer.load_program(t['program'])
        computer.set_inputs([t['input']])
        computer.execute()
        out = computer.get_output()
        if (out != t['output']):
            print("{}: {} != {}".format(i, out, t['output']))


if __name__ == "__main__":
    test_execute()
    pass