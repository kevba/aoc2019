
PUZZLE_INPUT_PATH = "../input.txt"

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, coord):
        return self.x == coord.x and self.y == coord.y

    def __lt__(self, coord):
        abs1 = abs(self.x) + abs(self.y) 
        abs2 = abs(coord.x) + abs(coord.y) 

        return abs1 < abs2

    def __str__(self):
        return "(x: {},y: {})".format(self.x,self.y)

    def get_relative_length(self, coord):
        if self.x == coord.x:
            return abs(self.y - coord.y)
        if self.y == coord.y:
            return abs(self.x - coord.x)
    
def line_to_coords(line):
    coords = [Coord(0,0)]
    for i, move in enumerate(line):
        previous_coord = coords[i]
        coord = ()

        moveInt = int_from_move(move)
        if "R" in move:
            coord = Coord(previous_coord.x+moveInt, previous_coord.y)
        if "L" in move:
            coord = Coord(previous_coord.x-moveInt, previous_coord.y)
        if "U" in move:
            coord = Coord(previous_coord.x, previous_coord.y+moveInt)
        if "D" in move:
            coord = Coord(previous_coord.x, previous_coord.y-moveInt)
        coords.append(coord)

    return coords

def int_from_move(move):
    numpart = move[1:]

    return int(numpart)


def find_collisions(wire1, wire2):
    collisions = []
    wire1_with_collisions = wire1.copy()
    wire2_with_collisions = wire2.copy()

    insertionOffset = 0

    for i in range(len(wire1)-1):
        w1p1 = wire1[i]
        w1p2 = wire1[i+1]


        for j in range(len(wire2)-1):
            w2p1 = wire2[j]
            w2p2 = wire2[j+1]

            coord = get_collision(w1p1,w1p2,w2p1,w2p2)

            if coord is not None:
                insertionOffset += 1

                collisions.append(coord)


    return (collisions, wire1_with_collisions, wire2_with_collisions)    

def is_between(x1, x2, val):
    if x1 <= val <= x2:
        return True
    if x2 <= val <= x1:
        return True
    
    return False

def find_quickest_path_length(wire1, wire2, collisions):
    fewest_steps = 999999999
    
    for c in collisions:
        path1_steps = get_path_to_collision(wire1, c)
        path2_steps = get_path_to_collision(wire2, c)

        steps = path1_steps + path2_steps
        if steps < fewest_steps:
            fewest_steps = steps

    return fewest_steps

def get_path_to_collision(wire, c):
    path = []
    for i, coord in enumerate(wire[:-1]):
        path.append(coord)
        
        if get_collision(coord,wire[i+1],c,c) is not None:
            path.append(c)
            break

    path = remove_loops(path)
    path_len = 0
    for i, coord in enumerate(path[:-1]):
        path_len += coord.get_relative_length(path[i+1]) 

    return path_len


def remove_loops(path):
    i=0
    new_path = []
    while i<len(path):
        coord = path[i]
        if coord in path[i+1:]:
            i = path[i+1:].index(coord)

        new_path.append(coord)
        i += 1

    return new_path

def get_collision(w1p1, w1p2, w2p1, w2p2):
    if is_between(w1p1.x, w1p2.x, w2p1.x):
        if is_between(w2p1.y, w2p2.y, w1p1.y):
            return Coord(w2p1.x, w1p1.y)

    if is_between(w2p1.x, w2p2.x, w1p1.x):
        if is_between(w1p1.y, w1p2.y, w2p1.y):
            return Coord(w1p1.x, w2p1.y)

    return None

def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    inputs = []
    with open(PUZZLE_INPUT_PATH) as f:
        for line in f.readlines():
            inputs.append(line.split(",")) 
    
    return inputs

if __name__ == "__main__":
    wires = read_puzzle_input()

    wire1 = line_to_coords(wires[0])
    wire2 = line_to_coords(wires[1])

    collisions, wire1, wire2 = find_collisions(wire1, wire2)

    # The fist coordinate is 0,0 for both wires.
    steps = find_quickest_path_length(wire1, wire2, collisions[1:])
    print(steps)
