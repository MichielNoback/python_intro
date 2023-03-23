
def read_file(file):
    '''Reads in the given data and returns a list of tuples,
    where each tuple contains exactly 3 numbers'''
    result = list()
    with open(file) as f:
        for line in f:
            print(f)
    return result

def process_numbers(numbers):
    '''Receives a list of tuples of 3 numbers each.
    Then calculates the first number divided by the second number, 
    and this times third number for each tuple.
    Returns a List of results.'''
    for t in numbers:
        pass

def main(args):
    '''Receives the command-line argument with file and 
    processes this with the two functions.
    Then reports the average of all processed cases.'''
    numbers = read_file(args[1])
    processed = process_numbers(numbers)


if __name__ == "__main__":
    '''main entry point'''
    import sys
    main(sys.argv)
