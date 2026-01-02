def get_filename() -> str:
    istxt = False
    while not istxt:
        filename = input('Enter name of document: ').strip()
        istxt = filename[-4:] == '.txt' and len(filename) > 4
        if not istxt:
            print('Provided filename is not a .txt file.')
    return filename

def get_init_dial_pos() -> int:
    isnum = False
    while not isnum:
        init_dial_pos = input('Enter initial dial position: ').strip()
        isnum = init_dial_pos.isdigit() and 0 <= int(init_dial_pos) <= 99
        if not isnum:
            print('Provided input is not an integer between 0 and 99, inclusive.')
    return int(init_dial_pos)

def get_protocol() -> str:
    is_protocol = False
    while not is_protocol:
        protocol = input('Choose protocol ("0" or "click"): ').strip().lower()
        is_protocol = protocol == '0' or protocol == 'click'
        if not is_protocol:
            print('Provided string does not match one of the listed protocols.')
    return protocol

def verify_document(filename: str) -> bool:
    with open(filename) as doc:
        return all((line.strip()[0].lower() == 'l' or 'r') and line.strip()[1:].isdigit() for line in doc)

def get_password(filename: str, init_dial_pos: int, protocol = get_protocol()) -> int:
    password = 0
    if verify_document(filename):
        with open(filename) as doc:
            parts = [[line.strip()[0].lower(), int(line.strip()[1:])] for line in doc]
    
    current_pos = init_dial_pos
    num_instructions = len(parts)
    for i in range(num_instructions):
        # Puzzle 1
        if protocol == '0':
            current_pos = (current_pos + parts[i][1] * (1 if parts[i][0] == 'r' else -1)) % 100
            password = password + (1 if current_pos == 0 else 0)
        # Puzzle 2
        else:
            # pos > 0
            # R, pos + rot < 100 -> + 0, pos = pos + rot (rot > 0)
            # R, pos + rot = 100 -> + 1, pos = 0
            # R, pos + rot > 100 -> + (pos + rot) // 100, pos = (pos + rot) % 100
            # L, abs(rot) < pos, -> + 0, pos = pos + rot (rot < 0)
            # L, rot = -pos, -> + 1, pos = 0
            # L, abs(rot) > pos, -> + abs(pos + rot) // 100, pos = (pos + rot) % 100
            # pos = 0
            # R, pos + rot -> + (pos + rot) // 100, pos = rot % 100
            # L, pos + rot -> abs(pos + rot) // 100, pos = rot % 100
            # L/R, rot = 0, pos = 0, -> + 0, pos = 0
            rotation = parts[i][1] * (1 if parts[i][0] == 'r' else -1)
            current_pos += rotation
            password = password + abs(current_pos) // 100 + (1 if current_pos <= 0 and current_pos - rotation != 0 else 0)
            current_pos %= 100

    return password

if __name__ == '__main__':
    print(f'Password: {get_password(filename = get_filename(), init_dial_pos = get_init_dial_pos())}')