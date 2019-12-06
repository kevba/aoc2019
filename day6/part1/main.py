
import math

PUZZLE_INPUT_PATH = "../input.txt"    

def parse(orbits):
    node_to_root = {}
    
    for orbit in orbits:
        o1, o2 = orbit.split(")")
        node_to_root[o2] = o1
    
    return node_to_root

def count_orbits(orbits, orbit):
    try:
        return count_orbits(orbits, orbits[orbit]) + 1    
    except KeyError:
        return 0

    return count_orbits(orbits, next_orbit) + 1    
    

def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    inputs = []
    with open(PUZZLE_INPUT_PATH) as f:
        lines = f.readlines()
        inputs = [orbit.strip() for orbit in lines]
    
    return inputs

if __name__ == "__main__":
    orbits = read_puzzle_input()
    tree = parse(orbits)
    
    answer = 0
    for orbit in tree:
        answer += count_orbits(tree, orbit)

    print(answer)