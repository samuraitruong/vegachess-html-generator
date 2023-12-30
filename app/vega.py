

import glob
import os
from playercard import process_player_card
from pairing import process_paring_file
from template import copy_css_and_js, get_template_str
from player import process_players_file, read_qtl_file
from standing import process_standings_file

def process_file(filename, out_dir, last_round, accumulate = {}):
    """
    Process a .qtf file based on its name.
    """
    ref = {
        "head_html": get_template_str('templates/head.html', {}),
        "nav_html": get_template_str('templates/nav.html', {"round": last_round, }),
        "pair_nav_html": get_template_str('templates/nav_pair.html', {"rounds": range(1, last_round + 1)})
    }
    qtl_content = read_qtl_file(filename)
    file_name_only = os.path.basename(filename)
    # Switch-case-like logic based on filename
    if file_name_only == "standings.qtf":
        accumulate['standings'] = process_standings_file(filename, out_dir, ref)
        # Your logic for file1.qtf
    elif file_name_only == "playerlist.qtf":
        accumulate['players'] = process_players_file(filename, out_dir, ref)
        # Your logic for file2.qtf
    elif "pairings" in file_name_only:
        pairing = process_paring_file(filename, out_dir, ref)
        accumulate["pairings"].append(pairing)
        # Your logic for file3.qtf
    else:
        print(f"Unhandled file: {filename}")
        accumulate['ref'] = ref

def main():
    """
    Main function to fetch and process .qtf files.
    """

    tournament_dir = 'Sample Tournament'
    tournament_dir = 'Demo Tournaments'
    out_dir = f'{tournament_dir}/www{tournament_dir}'
    # Fetch all .qtf files in the current directory.
    qtf_files = glob.glob(f"{tournament_dir}/*.qtf")
    pairing = [f for f in qtf_files if "pairings" in f]
    all_data = {
        "pairings" : []
    }
    # Loop through each .qtf file and process it.
    for qtf_file in qtf_files:
        process_file(qtf_file, out_dir, len(pairing), all_data)

    process_player_card(all_data, out_dir)

    copy_css_and_js(out_dir)
if __name__ == "__main__":
    main()
