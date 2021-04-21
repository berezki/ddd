import requests
import json


def get_mmr(player_id):
    player_id = int(player_id)
    url = 'https://api.opendota.com/api/players/{}'.format(player_id)
    response = requests.get(url).json()
    try:
        mmr = (response["mmr_estimate"]["estimate"])
        return mmr
    except KeyError:
        pass


def get_player_name(player_id):
    player_id = int(player_id)
    url = 'https://api.opendota.com/api/players/{}'.format(player_id)
    response = requests.get(url).json()
    try:
        player_name = (response["profile"]["personaname"])
        return player_name
    except KeyError:
        pass


def get_last_matches(player_id, page):

    offset = page * 10

    with open('data/heroes.json', encoding='utf-8') as her:
        heroes = json.load(her)

    matches = []
    matches_ids = []
    url = 'https://api.opendota.com/api/players/{}/matches?limit=10&offset={}'.format(str(player_id), offset)
    response = requests.get(url).json()

    for i in range(10):

        # заполнение массива matches именами героев
        for k in range(len(heroes)):
            if heroes[k]['id'] == response[i]['hero_id']:
                matches.append(heroes[k]['localized_name'])
                break

        # определение результата матча для игрока
        if (response[i]['player_slot'] < 100 and response[i]['radiant_win'])\
            or (response[i]['player_slot'] > 100 and not response[i]['radiant_win']):

            result = 'win'
        else:
            result = 'lose'

        # запоминание id матча
        matches_ids.append(response[i]['match_id'])

        # склеивание строки элемента массива
        matches[i] = '\n{}. {} {}/{}/{} {}'.format(
            str(i + 1),
            matches[i],
            str(response[i]['kills']),
            str(response[i]['deaths']),
            str(response[i]['assists']),
            result)

    return matches, matches_ids


def get_parameters_from_text(message: str, param_num=None):
    message = message.removeprefix(" ").removeprefix("!").removeprefix(" ")
    error = False
    
    parameters = message.split()
    if len(parameters) == 1:
        parameters = []
    else:
        parameters.pop(0)
    
    for i in range(len(parameters)):
        parameters[i] = parameters[i].removeprefix('-')

    if param_num is not None and len(parameters) != param_num:
        error = True
    return parameters, error


def get_match_information(match_id):
    url = 'https://api.opendota.com/api/matches/{}'.format(match_id)
    response = requests.get(url).json()
    with open('data/heroes.json', encoding='utf-8') as her:
        heroes = json.load(her)

    # вычисление времени в минуты
    duration = str(response['duration'] // 60) + ':' + str(response['duration'] % 60)

    players_ids = []
    players_in_match = []
    output = ''

    if response['radiant_win']:
        rad_win_status = ' - Win!'
        dir_win_status = ''
    else:
        rad_win_status = ''
        dir_win_status = ' - Win!'

    for i in range(10):

        players_ids.append(response['players'][i]['account_id'])

        kda = '{}/{}/{}'.format(
            str(response['players'][i]['kills']),
            str(response['players'][i]['deaths']),
            str(response['players'][i]['assists'])
        )

        # вычисление героев и формирование готовых строк для команды сил света
        try:
            for her in heroes:
                if her['id'] == response['players'][i]['hero_id']:
                    hero = her['localized_name']
                    break
            players_in_match.append('\n{}. {} - {} - {}'.format(
                str(i + 1),
                response['players'][i]['personaname'],
                hero,
                kda
            ))
        except KeyError:
            players_in_match.append('\n{}. Amonumous - {} - {}'.format(
                str(i + 1),
                hero,
                kda
            ))

    # мастер - строка
    output.append('\n\nRadiant team: {} {}'.fomrat(
        str(response['radiant_score']),
        rad_win_status
    ))
    
    for i  in range(5):
        output.append(players_in_match[i])

    output.append('\n\n{}\n\nDire team: {} {}'.fomrat(
        duration,
        str(response['dire_score']),
        dir_win_status
    ))

    for i in range(5, 10):
        output.append(players_in_match[i])


    return output, players_ids


def get_information_about_player_in_match(match_id, current_number):
    current_number = int(current_number)
    current_number -= 1
    url = 'https://api.opendota.com/api/matches/{}'.format(match_id)
    response = requests.get(url).json()
    with open('heroes.json', encoding='utf-8') as her:
        heroes = json.load(her)

    # строка с ником
    try:
        nickname = response['players'][current_number]['personaname']
    except:
        nickname = 'Anonumous'

    # строка с героем
    for i in range(len(heroes)):
        if heroes[i]['id'] == response['players'][current_number]['hero_id']:
            hero = heroes[i]['localized_name']
            break

    # строка с kda
    kda =   str(response['players'][current_number]['kills']) + '/' +\
            str(response['players'][current_number]['deaths']) + '/' + str(response['players'][current_number]['assists'])

    # строка с предметами
    items = ''
    for i in range(6):
        items += '\n' + str(response['players'][current_number]['item_' + str(i)])

    # нетворс
    net_worth = str(response['players'][current_number]['total_gold'])

    # склеиваем
    output = nickname + '\n' + hero + ' - ' + kda + '\n'
    output += 'Items:' + items

    return output, response['players'][current_number]['account_id']
