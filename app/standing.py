import re
import os
from template import output_standings_page

from share import get_value, read_qtl_file


def parse_standings_file(content):
    content = content.replace("[{_}%EN-US ", "").replace("[ {{", "")

    pattern = r"\[([^\]]*)\]"
    t = content.find('Tie Break legend')

    matches = re.findall(pattern, content[:t])
    # for x in matches:
    #     print(x)
    total_fields = len(matches[6:])
    headers = [get_value(v) for v in matches[5:15]]
    rows = []
    index = 15
    # print(headers)
    # headers= ["Bo", "White Fed", "White Player", "White Pts", "N1", "Result",  "N2", "Black Pts", "Black Player", "Black Fed"]
    for x in range(0, int((total_fields-10)/10)):
        item= {}
        for header in headers:
            item[header] = get_value(matches[index])
            index= index + 1

        rows.append(item)
    result = {
        "title": get_value(matches[1]),
        "sub_title": get_value(matches[2]),
        "sub_title1": get_value(matches[3]),
        "legend": [],
        "rows": rows,
        "headers": headers
    }
    
    return result

def process_standings_file(filename, out_dir, ref):
    qtl_content = read_qtl_file(filename)
        # Parse the QTL content
    standings = parse_standings_file(qtl_content)
    data = {**standings}
    data['ref'] = ref
    output_standings_page(data, out_dir)
    return standings

def main():
    # Get input filename from user
    filename =  "Sample Tournament/standings.qtf"
    # input("Enter the filename containing QTL content: ")
    
    try:
        # Read QTL content from file
        qtl_content = read_qtl_file(filename)
        # Parse the QTL content
        parsed_players = parse_standings_file(qtl_content)
        
        print(parsed_players)
        # Print the structured object
        #for row in parsed_players.get('rows'):
        #    print(row)
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")

if __name__ == "__main__":
    main()
