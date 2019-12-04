INPUT_START = 372037
INPUT_END = 905157


def is_valid(password):
    password = str(password)

    prev_c = password[0]
    password = password[1:]

    has_double = False
    is_valid = True

    for c in password:
        if prev_c == c :
            has_double = True
            continue
        if int(prev_c) > int(c):
            is_valid = False
            break

        prev_c = c
        
    return is_valid and has_double

if __name__ == "__main__":
    valids = []
    i = 0
    for inp in range(INPUT_START, INPUT_END):
        if is_valid(inp):
            valids.append(inp)
    
    print(len(valids))

    