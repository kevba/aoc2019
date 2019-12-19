import timeit

PUZZLE_INPUT_PATH = "../input.txt"

class ChemFactory():
    def __init__(self, recipies):
        self.recipies = recipies
        self.resources = {}

        self.total_produced = {}
        self.ore_counter = 0

    def build_chemical(self, name, amount):
        if name == "ORE":
            self.ore_counter += amount
            return

        components = self.recipies[name]["components"]
        result_count = self.recipies[name]["result"]["amount"]

        amount_counter = self.resources.get(name, 0)

        while amount_counter < amount:
            for c in components:
                self.build_chemical(c["name"], c["amount"])
            amount_counter += result_count

        self.resources[name] = amount_counter - amount

    def ore_to(self, name, ore_count):
        self.build_chemical(name, 1)
        ore_per = self.ore_counter

        counter = ore_count // ore_per
        remaining_ore = ore_count % ore_per
        
        self.ore_counter = 0

        while True:
            self.build_chemical(name, 1)
            if self.ore_counter > remaining_ore:
                return counter

            counter +=1


def chem_from_string(s):
    cc_parts = s.split(" ")
    name = cc_parts[1].strip()
    amount = int(cc_parts[0].strip())

    return {
        "name": name,
        "amount": amount,
    }

def read_puzzle_input():
    recipies = {}

    with open(PUZZLE_INPUT_PATH) as f:
        for line in f.readlines():
            parts = line.split(" => ")

            component_strings = parts[0].split(", ")
            components = []
            for cc in component_strings:
                components.append(chem_from_string(cc))

            result = chem_from_string(parts[1])
            recipies[result["name"]] = {"result": result, "components": components}

    return recipies

def solve():
    chemicals = read_puzzle_input()

    fac = ChemFactory(chemicals)

    print(fac.ore_to("FUEL", 1000000000000))

if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))