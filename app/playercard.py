from template import output_playercard_page


def process_player_card(data, out_dir):
    
    playercard_data = {
        "ref": data['ref'],
        "title": data['standings']['title'],
        "sub_title": data['standings']['sub_title'],
        "rows": data['players']['rows'],
        "headers": ["R", "C", "N", "CAT", "Opponent", "Rtg", "Result", "Pts"]
    }
    pairings = data['pairings']
    player_rtg ={}

    for player in  data['players']['rows']:
        player_rtg[player['Name']] = player['NRtg']
        player_rtg[player['Title'] + ' ' +player['Name']] = player['NRtg']
    for row in playercard_data['rows']:
        row['pairs'] = []
        for pr in pairings:
            for r in pr['rows']:
                player_name = row['Name']
                
                if player_name in r['White Player']:

                    row['pairs'].append({
                        "R": pr['round'],
                        'C': 'W',
                        "CAT": '',
                        'Opponent':r['Black Player'],
                        "Result": r['Result'],
                        "Rtg": player_rtg[r['Black Player']],
                        "Pts":  r['White Pts']
                    })
                if player_name in r['Black Player']:
                    row['pairs'].append({
                        "R": pr['round'],
                        'C': 'B',
                        "CAT": '',
                        'Opponent':r['White Player'],
                        "Result": r['Result'],
                        "Rtg": player_rtg[r['White Player']],
                        "Pts": r['Black Pts']
                    })
        row['pairs'].sort(key=lambda x:x['R'])
    output_playercard_page(playercard_data, out_dir)