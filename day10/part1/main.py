import timeit

PUZZLE_INPUT_PATH = "../input.txt"


class Asteroid():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.blocked_paths = []
        self.visible_counter = 0
    
    def set_visible(self, asteroid):    
        if self == asteroid:
            return
    
        for is_blocked in self.blocked_paths:
            if is_blocked(asteroid.x, asteroid.y):
                return
        
        self.handle_visible(asteroid)
    
    def handle_visible(self,asteroid):
        self.visible_counter += 1

        f = self.create_path_fomula(asteroid.x, asteroid.y)

        self.blocked_paths.append(f)

    def create_path_fomula(self, x2, y2):
        if (x2 - self.x) == 0:
            return lambda x, y:  x == self.x        

        if (y2 - self.y) == 0:
            return lambda x, y:  y == self.y         

        lin = lambda x: ((y2 - self.y) / (x2 - self.x))*x

        if self.x > x2 and self.y > y2:
            is_blocked = lambda x, y: lin(x) == y and x > self.x and y > self.y  
        if self.x < x2 and self.y > y2:
            is_blocked = lambda x, y: lin(x) == y and x < self.x and y > self.y  
        if self.x > x2 and self.y < y2:
            is_blocked = lambda x, y: lin(x) == y and x > self.x and y < self.y  
        if self.x < x2 and self.y < y2:
            is_blocked = lambda x, y: lin(x) == y and x < self.x and y < self.y  

        # return lambda x, y: lin(x) < y+1 and lin(x) > y-1         
        return is_blocked

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    with open(PUZZLE_INPUT_PATH) as f:
        return [[r for r in row.rstrip()] for row in f.readlines()]

def solve():
    asteroid_input = read_puzzle_input()
    asteroids = []

    for y, a_row in enumerate(asteroid_input):
        for x, a in enumerate(a_row):
            if a == '#':
                asteroids.append(Asteroid(x, y))
    
    for a in asteroids:
        for b in asteroids:
            a.set_visible(b)
    
    most_visible_counter = 0
    most_visible_index = 0
    for i, a in enumerate(asteroids):
        if a.visible_counter > most_visible_counter:
            most_visible_counter = a.visible_counter
            most_visible_index = i
    
    print(asteroids[most_visible_index].visible_counter, asteroids[most_visible_index].x+1, asteroids[most_visible_index].y+1 )


if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))