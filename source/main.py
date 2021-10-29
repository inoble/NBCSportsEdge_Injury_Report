import urllib.request, json, datetime
from info import nbc_sports_edge_team_ids

team_id_list = nbc_sports_edge_team_ids.team_ids

print ('Pulling injury data... ')

for team in team_id_list:

    try:

        first_half_of_team_url = "https://www.nbcsportsedge.com/edge/api/injury?sort=-start_date&filter%5Bplayer.team.meta.drupal_internal__id%5D="
        second_half_of_team_url = "&filter%5Bplayer.status.active%5D=1&filter%5Bactive%5D=1&include=injury_type,player,player.status,player.position"
        team_url = first_half_of_team_url + str(team) + second_half_of_team_url
        url = urllib.request.urlopen(team_url)

        data = json.loads(url.read().decode())
        injuries_json = data['data']
        players_json = data['included']

        number_of_injuries = len(injuries_json)
        number_of_included_keys = len(players_json)

        # Match player_ids in injury and player listings of the same JSON file, pull Name, Unique Injury ID and calculate length of injury
        for x in range(number_of_injuries):

            player_id = injuries_json[x]['relationships']['player']['data']['id']
            injury_id = injuries_json[x]['id']

            # injury_start_date is converted into datetime format so that duration can be calculated
            injury_start_date = datetime.datetime.strptime(injuries_json[x]['attributes']['start_date'], '%Y-%m-%d').date()

            for x in range(number_of_included_keys):

                found_player_id = players_json[x]['id']

                if player_id == found_player_id:
                
                    player_name = players_json[x]['attributes']['name']

                    length_of_injury = (datetime.date.today() - injury_start_date).days

            print (player_name + ' | Injury ID: ' + injury_id + ' | Duration: ' + str(length_of_injury))
    
    except KeyError:

        pass