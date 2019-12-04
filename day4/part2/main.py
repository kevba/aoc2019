INPUT_START = 372037
INPUT_END = 905157


def is_valid(input_password):
    password = str(input_password)


    has_double = has_valid_double(password)
    is_valid = True

    prev_c = password[0]
    for i, c in enumerate(password[1:]):
        if int(prev_c) > int(c):
            is_valid = False
            break

        prev_c = c
        
    return is_valid and has_double


def has_valid_double(password):
    char_counter = 0
    max_chars = 2

    char = password[0]
    for c in password[1:]:
        if c == char:
            char_counter += 1
        elif c != char:
            if char_counter == max_chars-1:
                return True
            char_counter = 0

        char = c

    if char_counter == max_chars-1:
        return True

    return False
    

if __name__ == "__main__":
    valids = []
    for inp in range(INPUT_START, INPUT_END):
        if is_valid(inp):
            valids.append(inp)
    
    print(len(valids))

    