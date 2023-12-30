import re
from template import output_players_page

from share import get_value


def parse_player_file(content):
    pattern = r"\[([^\]]*)\]"
    
    matches = re.findall(pattern, content)
    total_fields = len(matches[2:])
    headers = [get_value(v) for v in matches[2:8]]
    players = []
    index = 8
    for x in range(0, int((total_fields-6)/6)):
        item= {}
        for header in headers:
            item[header] = get_value(matches[index])
            index= index + 1

        players.append(item)
    player_result = {
        "title": get_value(matches[0]),
        "sub_title": get_value(matches[1]),
        "rows": players,
        "headers": headers,
    }
    
    return player_result

def read_qtl_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def process_players_file(filename, out_dif, ref):
    qtl_content = read_qtl_file(filename)
        # Parse the QTL content
    players = parse_player_file(qtl_content)
    data = {**players}
    data['ref'] = ref
    output_players_page(data, out_dif)
    return players
     

def main():
    # Get input filename from user
    filename =  "/Users/truongnguyen/truong/git/vegachess-html-generator/Sample Tournament/playerlist.qtf"
    # input("Enter the filename containing QTL content: ")
    
    try:
        # Read QTL content from file
        qtl_content = read_qtl_file(filename)
        # Parse the QTL content
        parsed_players = parse_player_file(qtl_content)
        
        print(parsed_players)
        # Print the structured object
        for player in parsed_players.get('players'):
            print(player)
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")

if __name__ == "__main__":
    main()
