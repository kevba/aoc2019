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
    
    def is_blocked(self, a):
        for va in self.visible_asteroids:
            lin = self.create_path_fomula(va.x, va.y)
            try:
                if lin(a.x) == a.y:
                    return True
            except ZeroDivisionError:
                if self.x == va.x == a.x:
                    return True
        return False

    def create_path_fomula(self, x2, y2):
        lin = lambda x: ((y2 - self.y) / (x2 - self.x))*x

        # if (x2 - self.x) == 0 and  y2 > self.y:
        #     return lambda x, y:  x == self.x and y > self.y
        # elif (x2 - self.x) == 0 and y2 < self.y:
        #     return lambda x, y:  x == self.x and y < self.y

        # lin = lambda x: ((y2 - self.y) / (x2 - self.x))*x

        # if self.x > x2 and y2 >= self.y:
        #     is_blocked = lambda x, y: lin(x) == y and x > self.x and y >= self.y  
        # elif self.x < x2 and y2 >= self.y:
        #     is_blocked = lambda x, y: lin(x) == y and x < self.x and y >= self.y  
        # elif self.x > x2 and y2 <=  self.y:
        #     is_blocked = lambda x, y: lin(x) == y and x > self.x and y <= self.y  
        # elif self.x < x2 and y2 <= self.y :
        #     is_blocked = lambda x, y: lin(x) == y and x < self.x and y <= self.y  
        # # return lambda x, y: lin(x) < y+1 and lin(x) > y-1         
        return lin



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