import re
import os
from template import output_pairings_page

from share import get_value, read_qtl_file


def parse_pairing_file(content):
    pattern = r"\[([^\]]*)\]"
    
    matches = re.findall(pattern, content)
    total_fields = len(matches[2:])
    headers = [get_value(v) for v in matches[2:12]]
    rows = []
    index = 12
    headers= ["Bo", "White Fed", "White Player", "White Pts", "NW", "Result",  "NB", "Black Pts", "Black Player", "Black Fed"]
    for x in range(0, int((total_fields-10)/10)):
        item= {}
        for header in headers:
            item[header] = get_value(matches[index])
            index= index + 1

        rows.append(item)
    player_result = {
        "title": get_value(matches[0]),
        "sub_title": get_value(matches[1]),
        "rows": rows,
        "headers": headers
    }
    
    return player_result

def process_paring_file(filename, out_dir, ref):
    qtl_content = read_qtl_file(filename)
        # Parse the QTL content
    parsed_data = parse_pairing_file(qtl_content)
    data = {**parsed_data}
    data['ref'] = ref
    index = re.search('(\d+)', filename)
    data['round'] = index.group(1)
    output_pairings_page(data, out_dir)

    return data

def main():
    # Get input filename from user
    filename =  "Sample Tournament/pairings2.qtf"
    # input("Enter the filename containing QTL content: ")
    
    try:
        # Read QTL content from file
        qtl_content = read_qtl_file(filename)
        # Parse the QTL content
        parsed_players = parse_pairing_file(qtl_content)
        
        print(parsed_players)
        # Print the structured object
        for row in parsed_players.get('rows'):
            print(row)
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")

if __name__ == "__main__":
    main()
