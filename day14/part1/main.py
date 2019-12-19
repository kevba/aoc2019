import timeit

PUZZLE_INPUT_PATH = "../input.txt"


class Chemical():
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash("{}".format(self.name))


def chem_from_string(s):
    cc_parts = s.split(" ")
    name = cc_parts[1].strip()
    amount = int(cc_parts[0].strip())

    return Chemical(name, amount)

def read_puzzle_input():
    inputs = {}

    with open(PUZZLE_INPUT_PATH) as f:
        for line in f.readlines():
            parts = line.split(" => ")

            component_strings = parts[0].split(", ")
            components = []
            for cc in component_strings:
                components.append(chem_from_string(cc))

            result = chem_from_string(parts[1])
            inputs[result.name] = {"result": result, "components": components}
    return inputs

def ore_counter(chemicals, chem_to_create, amount, i=0):
    i += 2
    print(" "*i, chem_to_create, amount)
    if chem_to_create == "ORE":
        return amount

    ore_amount = 0
    amount_counter = 0

    components = chemicals[chem_to_create]["components"]
    amount_created = chemicals[chem_to_create]["result"].amount

    while amount_counter < amount:
        for c in components:
            
            ore_amount += ore_counter(chemicals, c.name, c.amount, i)
        amount_counter += amount_created

    return ore_amount

def solve():
    chemicals = read_puzzle_input()

    fuel = None
    
    ore_count = ore_counter(chemicals, "FUEL", 1)
    print(ore_count)

if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))