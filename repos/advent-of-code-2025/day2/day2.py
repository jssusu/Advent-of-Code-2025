def get_filename() -> str:
    istxt = False
    while not istxt:
        filename = input('Enter name of document: ').strip()
        istxt = filename[-4:] == '.txt' and len(filename) > 4
        if not istxt:
            print('Provided filename is not a .txt file.')
    return filename

def verify_string(filename: str) -> bool:
    with open(filename) as file:
        line = file.read().strip()
        if line.count('\n') > 0:
            return False
        
    ranges_short = line.split(',')
    ranges = [ranges_short[i].split('-') for i in range(len(ranges_short))]
    return all(len(ranges[j]) == 2 and all(number.isdigit() for number in ranges[j]) 
               and all(int(ranges[j][i]) < int(ranges[j][i + 1]) for i in range(len(ranges[j]) - 1)) for j in range(len(ranges)))

def get_ranges(filename: str) -> list[list[int]]:
    if verify_string(filename):
        with open(filename) as file:
            ranges_short = file.read().strip().split(',')
        return [ranges_short[i].split('-') for i in range(len(ranges_short))]

def sum_invalid_ids(filename: str) -> int:
    ranges = get_ranges(filename)
    sum = 0
    for i in range(len(ranges)):
        for j in range(int(ranges[i][0]), int(ranges[i][1]) + 1):
            if len(str(j)) % 2 != 0:
                continue
            number = str(j)
            midpoint = int(len(number) / 2)
            if number[:midpoint] == number[midpoint:]:
                sum += j
    return sum

if __name__ == '__main__':
    print(f'Sum: {sum_invalid_ids(filename = get_filename())}')