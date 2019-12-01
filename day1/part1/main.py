
import math

PUZZLE_INPUT_PATH = "../input.txt"

DIVIDER = 3
SUBTRACTOR = 2

def calculate_fuel_for_unit(unit_mass):
    """  Takes the mass of the unit and calculates the fuel needed.

    :param unit_mass: Mass of the unit.
    :returns: Required fuel.
    """
    fuel = (math.floor(unit_mass / 3)) - 2
    return fuel

def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    inputs = []
    with open(PUZZLE_INPUT_PATH) as f:
        lines = f.readlines()
        inputs = [int(mass) for mass in lines]
    
    return inputs

if __name__ == "__main__":
    masses = read_puzzle_input()

    total_fuel_required = 0

    for mass in masses:
        fuel = calculate_fuel_for_unit(mass)
        total_fuel_required += fuel
    
    print(total_fuel_required)