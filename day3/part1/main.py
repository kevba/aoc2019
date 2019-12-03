
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


def find_collisions(wire1, wire2):
    collisions = []

    for i in range(len(wire1)-1):
        for j in range(len(wire2)-1):
            collision = Coord(-1,-1)

            w1p1 = wire1[i]
            w1p2 = wire1[i+1]

            w2p1 = wire2[j]
            w2p2 = wire2[j+1]

            if is_between(w1p1.x, w1p2.x, w2p1.x):
                if is_between(w2p1.y, w2p2.y, w1p1.y):
                    collisions.append(Coord(w2p1.x, w1p1.y))
                    continue

            if is_between(w2p1.x, w2p2.x, w1p1.x):
                if is_between(w1p1.y, w1p2.y, w2p1.y):
                    collisions.append(Coord(w1p1.x, w2p1.y))
                    continue

    return collisions    

def is_between(x1, x2, val):
    if x1 <= val <= x2:
        return True
    if x2 <= val <= x1:
        return True
    
    return False

def find_smallest_distance(coords):
    smallest = coords[0]

    for c in coords:
        if c < smallest:
            smallest = c
    
    return smallest

def int_from_move(move):
    numpart = move[1:]

    return int(numpart)


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

    # The fist coordinate is 0,0 for both wires.
    collisons = find_collisions(wire1[1:], wire2[1:])

    smallest = find_smallest_distance(collisons)

    distance = abs(smallest.x+smallest.y)
    print(smallest, distance)



