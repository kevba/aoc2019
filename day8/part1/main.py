import timeit

PUZZLE_INPUT_PATH = "../input.txt"

class Image():
    def __init__(self, encoded, width=25, height=6):
        self.width = width
        self.height = height

        self.layers = []
        self.to_layers(encoded)
    
    def to_layers(self, encoded):
        layer_size = self.width*self.height 
        layer = []
        layers = []
        for p in encoded:
            layer.append(p)
            if len(layer) >= layer_size :
                layers.append(layer)
                layer = []
        
        self.layers = layers
    
    def check_image(self):        
        least_index = 0
        least_count = 999999999 

        for i, layer in enumerate(self.layers):
            zero_count = len([d for d in layer if d == 0])
            if  zero_count < least_count:
                least_count = zero_count
                least_index = i

        ones = len([d for d in self.layers[least_index] if d == 1])
        twos = len([d for d in self.layers[least_index] if d == 2])

        # print(least_index, least_count, ones, twos)
        # print(self.layers[least_index])

        return ones * twos


def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    with open(PUZZLE_INPUT_PATH) as f:
        return [int(d) for d in f.readline() if d.isdigit()]

def solve():
    encoded_image = read_puzzle_input()

    img = Image(encoded_image)
    print(img.check_image())
    pass

if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))