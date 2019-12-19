import timeit

from itertools import permutations

import re

MOON_NAMES = ["Io", "Europa", "Ganymede", "Callisto"]
STEPS = 1000
current_step = 0

class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash("{}_{}_{}".format(self.x, self.y, self.z))

class Velocity():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def apply(self, point):
        point.x += self.x
        point.y += self.y
        point.z += self.z

        return point

    def invert(self):
        return Velocity(0-self.x,0-self.y,0-self.z)

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Moon():
    def __init__(self, position, name="Deathstar"):
        self.position = position
        self.name = name

        self.velocity = Velocity()
    
    def update_velocity(self, velocity):
        self.velocity + velocity

    def apply_velocities(self):
        self.position = self.velocity.apply(self.position)

    def potential_energy(self):
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

    def kinetic_energy(self):
        return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def __str__(self):
        return "{}: position: {} - velocity: {}".format(self.name, self.position, self.velocity)

    def __eq__(self, other):
        return self.position == other.position and self.velocity == other.velocity

PUZZLE_INPUT_PATH = "../input.txt"

def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """

    regexp = re.compile(r"([xyz])=(-?[0-9]*)")
    inputs = []

    with open(PUZZLE_INPUT_PATH) as f:
        for line in f.readlines():
            inputs.append({m[0]: int(m[1]) for m in regexp.findall(line)})

    return inputs

def calculate_gravity(moons):
    for moons in permutations(moons, 2):
        v = Velocity()
        if moons[0].position.x > moons[1].position.x:
            v.x = 1
        if moons[0].position.y > moons[1].position.y:
            v.y = 1
        if moons[0].position.z > moons[1].position.z:
            v.z = 1

        moons[0].update_velocity(v.invert())
        moons[1].update_velocity(v)

def update(moons, current_step):
    for m in moons:
        m.apply_velocities()

def calculate_total_energy(moons):
    system_total_energy = 0
    for m in moons:
        system_total_energy += m.total_energy()

    return system_total_energy

def print_step_log(moons, step):
    print("after {} steps ----------------------------------".format(step))
    for m in moons:
        print(m)
    print("total energy: {}".format(calculate_total_energy(moons)))
    print("")

def moons_are_equal(moons1, moons2):
    for i, m in enumerate(moons1):
        if m != moons2[i]:
            return False

    return True

def solve():
    moon_data = read_puzzle_input()

    moons = []
    og_moons = []
    for i, m in enumerate(moon_data):
        pos = Point(m["x"], m["y"], m["z"])
        moons.append(Moon(pos, MOON_NAMES[i]))
        og_moons.append(Moon(pos, MOON_NAMES[i]))

    current_step = 0
    while True:
        current_step += 1
        calculate_gravity(moons)
        update(moons, current_step)

    print(current_step)

if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))