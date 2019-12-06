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
        return count_orbits(orbits, orbits[orbit]) + 1    
    except KeyError:
        return 0
    

def find_path_to_root(orbits, orbit):
    try:
        path = (find_path_to_root(orbits, orbits[orbit]))
        path.append(orbit)
        return path
    except KeyError:
        path = [orbit]
        return path

def remove_common_path(path1, path2):
    for i in range(len(path1)):
        if path1[i] != path2[i]:
            return (path1[i:],path2[i:])


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
    orbitLines = read_puzzle_input()
    orbits = parse(orbitLines)

    you_root_path = find_path_to_root(orbits, "YOU")  
    santa_root_path = find_path_to_root(orbits, "SAN")  
    
    you_root_path, santa_root_path = remove_common_path(you_root_path, santa_root_path)
    total_distance = len(you_root_path) + len(santa_root_path)
    # Remove the jumps from YPOU and SANTA
    required_jumps = total_distance - 2
    print(required_jumps)

if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))