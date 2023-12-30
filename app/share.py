import re

def get_value(input):
    index = input.find(' ')
    # arr= re.split(r"\s", str(input), 1)
    return input[index+1:].replace("&", "").strip()

def read_qtl_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content