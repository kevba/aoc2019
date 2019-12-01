
import math

PUZZLE_INPUT_PATH = "../input.txt"

DIVIDER = 3
SUBTRACTOR = 2

def calculate_fuel_for_unit(unit_mass):
    """  Takes the mass of the unit and calculates the fuel needed.

    :param unit_mass: Mass of the unit.
    :returns: Required fuel.
    """
    fuel = calculate_fuel(unit_mass)

    fuel += calculate_fuel_for_fuel(fuel)
    return fuel

def calculate_fuel_for_fuel(fuel_mass):
    """  Takes the mass of the fuel and calculates the fuel needed.

    :param fuel_mass: Mass of the fuel.
    :returns: Required fuel.
    """
    additional_fuel = fuel_mass
    total_fuel_required = 0
    
    while True:
        additional_fuel = calculate_fuel(additional_fuel)
        if additional_fuel <= 0:
            break

        total_fuel_required += additional_fuel

    return total_fuel_required

def calculate_fuel(mass):
    """  Takes a mass and calculates the fuel needed.

    :param mass: Mass of the unit or fuel.
    :returns: Required fuel.
    """
    fuel = (math.floor(mass / 3)) - 2
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