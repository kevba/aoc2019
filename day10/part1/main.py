import timeit
import math 
from fractions import Fraction

PUZZLE_INPUT_PATH = "../input.txt"
ASTEROIDS = []
MAX_WIDTH = 0
MAX_LENTH = 0

class Asteroid():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.atans_1 = []
        self.atans_2 = []
        self.atans_3 = []
        self.atans_4 = []

    def set_visible_asteroids(self):
        sorted_by_distance = ASTEROIDS.copy()
        sorted_by_distance.sort()
        
        for a in sorted_by_distance:
            if a is self:
                continue

            atan = math.atan2(a.x-self.x, a.y-self.y)

            if a.x >= self.x and a.x >= self.x:
                if atan not in self.atans_1:
                    self.atans_1.append(atan)
            elif a.x > self.x and a.x < self.x:
                if atan not in self.atans_2:
                    self.atans_2.append(atan)
            elif a.x < self.x and a.x > self.x:
                if atan not in self.atans_3:
                    self.atans_3.append(atan)
            elif a.x < self.x and a.x < self.x:
                if atan not in self.atans_4:
                    self.atans_4.append(atan)

    def all_atans(self):
        atts = []
        atts.extend(self.atans_1)
        atts.extend(self.atans_2)
        atts.extend(self.atans_3)
        atts.extend(self.atans_4)

        return atts

    def count(self):
        return len(self.all_atans())

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
                ASTEROIDS.append(Asteroid(x+1, y+1))
    
    for a in ASTEROIDS:
        a.set_visible_asteroids()
    
    most_visible_counter = 0
    most_visible = None
    for i, a in enumerate(ASTEROIDS):
        if a.count() > most_visible_counter:
            most_visible_counter = a.count()
            most_visible_i = i
            most_visible = a
    
    print(most_visible_counter, most_visible_i, a.x, a.y)


if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))