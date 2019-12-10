import timeit
import math 

PUZZLE_INPUT_PATH = "../input.txt"
ASTEROIDS = []

class Asteroid():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.visible_asteroids = []

    def set_visible_asteroids(self):
        sorted_by_distance = ASTEROIDS.copy()
        sorted_by_distance.sort()
        for a in sorted_by_distance:
            if a is self:
                continue
            if not self.is_blocked(a):
                self.visible_asteroids.append(a)

    
    def is_blocked(self, asteroid):
        for va in self.visible_asteroids:
            if abs(va.x - asteroid.x) == abs(self.x - va.x):
                if abs(va.y - asteroid.y) == abs(self.y - va.y):
                    return True
        return False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, coord):
        abs1 = abs(self.x) + abs(self.y) 
        abs2 = abs(coord.x) + abs(coord.y) 

        return abs1 < abs2

def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    with open(PUZZLE_INPUT_PATH) as f:
        return [[r for r in row.rstrip()] for row in f.readlines()]

def solve():
    asteroid_input = read_puzzle_input()

    for y, a_row in enumerate(asteroid_input):
        for x, a in enumerate(a_row):
            if a == '#':
                ASTEROIDS.append(Asteroid(x, y))
    
    for a in ASTEROIDS:
        a.set_visible_asteroids()
    
    most_visible_counter = 0

    for i, a in enumerate(ASTEROIDS):
        if len(a.visible_asteroids) > most_visible_counter:
            most_visible_counter = len(a.visible_asteroids)
    
    print(most_visible_counter)


if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))