import timeit
import math

PUZZLE_INPUT_PATH = "../input.txt"    

distance_to_root = {}

def parse(orbits):
    node_to_root = {}
    
    for orbit in orbits:
        o1, o2 = orbit.split(")")
        node_to_root[o2] = o1
    
    return node_to_root

def count_orbits(orbits, orbit):
    try:
        root_distance = distance_to_root.get(orbit, -1)
        if  root_distance > -1:
            return root_distance
    
        root_distance =  count_orbits(orbits, orbits[orbit]) + 1
        distance_to_root[orbit] = root_distance
        return root_distance
    except KeyError:
        return 0
    

def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    inputs = []
    with open(PUZZLE_INPUT_PATH) as f:
        lines = f.readlines()
        inputs = [orbit.strip() for orbit in lines]
    
    return inputs

def solve():
    orbits = read_puzzle_input()

    tree = parse(orbits)
    
    answer = 0
    for orbit in tree:
        answer += count_orbits(tree, orbit)

    print(answer)

if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))