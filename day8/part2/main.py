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

        return ones * twos

    def get_squashed(self):
        squashed = [-1] * (self.width*self.height)

        for l in self.layers:
            for i, p in enumerate(l):
                if p == 2:
                    continue
                if squashed[i] == -1:
                    squashed[i] = p
        
        return squashed

    def render_to_console(self):
        img  = self.get_squashed()
        img_str = ""

        for i, p in enumerate(img):
            if i % self.width == 0:
                img_str = img_str + '\n'

            if p == 1:
                img_str = img_str + '#'
            else:
                img_str = img_str + ' '
    
        print(img_str)

def read_puzzle_input():
    """ Reads the puzzle input and returns it a list.

    :returns: A list where each item is an input.
    """
    with open(PUZZLE_INPUT_PATH) as f:
        return [int(d) for d in f.readline() if d.isdigit()]

def solve():
    encoded_image = read_puzzle_input()

    img = Image(encoded_image)
    img.render_to_console()

if __name__ == "__main__":
    execution_time = timeit.timeit(solve, number=1)
    print("{} s".format(execution_time))