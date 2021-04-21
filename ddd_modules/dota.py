import json
from vk_api.utils import get_random_id
from ddd_modules import analyzer, invoker
import yaml


def dota_check(event, vk, sessions, players, longpoll):

    def send_last_matches(player_id, page):
        matches = analyzer.get_last_matches(player_id, page)

        # получение айдишников матчей, которые будут выведены
        sessions[str(event.obj.peer_id)]["current_match_ids"] = matches[1]

        page = sessions[str(event.obj.peer_id)]['matches_page']

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=matches[0],
            random_id=get_random_id()
        )

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='Страница {}'.format(page + 1),
            random_id=get_random_id()
        )

    if event.obj.text.casefold() == '!session' or event.obj.text.casefold() == '! session':

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=yaml.dump(sessions[str(event.obj.peer_id)]),
            random_id=get_random_id()
        )

    elif event.obj.text.casefold() == '!players' or event.obj.text.casefold() == '! players':

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=yaml.dump(players),
            random_id=get_random_id()
        )

    elif '!match_' in event.obj.text.casefold() or '! match_' in event.obj.text.casefold():

        # считывание match_id из сообщения
        match_id, error = analyzer.get_parameters_from_text(event.obj.text, 1)

        # проверка на ошибку с параметрами
        if not error:
            # передача в сессию
            sessions[str(event.obj.peer_id)]['match_id'] = match_id[0]
            # match_id берет уже из сессии данной конфы
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='считанный id: {}'.format(sessions[str(event.obj.peer_id)]['match_id']),
                random_id=get_random_id()
            )
        else:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Использование: !match -match_id',
                random_id=get_random_id()
            )

    elif '!player' in event.obj.text.casefold() or '! player' in event.obj.text.casefold():

        # считывание player_id
        player_id, error = analyzer.get_parameters_from_text(event.obj.text, 1)

        # проверка на ошибки считывания
        if not error:
            # передача в сессию
            sessions[str(event.obj.peer_id)]['player_id'] = player_id[0]

            # получение из сессии
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='считанный id: {}'.format(sessions[str(event.obj.peer_id)]['player_id']),
                random_id=get_random_id()
            )

        else:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Использование: !player: -player_id',
                random_id=get_random_id()
            )

    elif '!mmr' in event.obj.text.casefold() or '! mmr' in event.obj.text.casefold():
        error = False
        parameters = analyzer.get_parameters_from_text(event.obj.text)[0]

        if len(parameters) == 0:
            mmr = analyzer.get_mmr(sessions[str(event.obj.peer_id)]['player_id'])

        elif len(parameters) == 1:
            if parameters[0] == 'mystat':
                mmr = analyzer.get_mmr(players[str(event.obj.from_id)]['player_id'])
            else:
                mmr = analyzer.get_mmr(parameters[0])

        else:
            error = True

        if error:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Использование: !mmr (ммр текущего игрока) или !mmr -player-id (ммр игрока player-id)',
                random_id=get_random_id()
            )

        else:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Ваш ммр: {}'.format(mmr),
                random_id=get_random_id()
            )

    elif '!matches' in event.obj.text.casefold() or '! matches' in event.obj.text.casefold():
        error = False
        parameters = analyzer.get_parameters_from_text(event.obj.text)[0]

        sessions[str(event.obj.peer_id)]['current_flags']['matches'] = True
        sessions[str(event.obj.peer_id)]['current_flags']['players'] = False

        sessions[str(event.obj.peer_id)]['matches_page'] = 0

        if len(parameters) == 0:
            player_name = analyzer.get_player_name(sessions[str(event.obj.peer_id)]["player_id"])
            player_id = sessions[str(event.obj.peer_id)]["player_id"]
        elif len(parameters) == 1:
            if parameters[0] == 'mystat':
                player_name = analyzer.get_player_name(players[str(event.obj.from_id)]['player_id'])
                player_id = players[str(event.obj.from_id)]['player_id']
                sessions[str(event.obj.peer_id)]['player_id'] = player_id
            else:
                player_id = parameters[0]
                player_name = analyzer.get_player_name(player_id)
                sessions[str(event.obj.peer_id)]['player_id'] = player_id
        else:
            error = True

        if error:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Использование: !matches (игры текущего игрока) или !matches -player_id (игры игрока player_id)',
                random_id=get_random_id()
            )

        else:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message=player_name,
                random_id=get_random_id()
            )

            send_last_matches(player_id, sessions[str(event.obj.peer_id)]['matches_page'])

    elif event.obj.text.casefold() == '!newsession' or event.obj.text.casefold() == '! newsession':

        # добавление новой сессии
        sessions[str(event.obj.peer_id)] = {'peer_id': event.obj.peer_id,
                                            'match_id': '',
                                            'player_id': '',
                                            'current_match_ids': [],
                                            'current_player_ids': [],
                                            'current_flags': {  'matches': False,
                                                                'players': False,
                                                                'invoke': False,
                                                                'casino_notifications_enabled': True},
                                            "matches_page": None
                                            }

        # сохранение файлла сессии на диск
        with open('data/sessions.json', 'w', encoding='utf-8', ) as ses:
            json.dump(sessions, ses, indent=4)

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='Успешно!',
            random_id=get_random_id()
        )

    elif '!newplayer' in event.obj.text.casefold() or '! newplayer' in event.obj.text.casefold():
        if str(event.obj.from_id) in players:
            msg_output = 'Ты уже в базе, дорогуша'
        else:
            parameters, error = analyzer.get_parameters_from_text(event.obj.text)

            if len(parameters) == 0:
                players[str(event.obj.from_id)] = { 'vk_id': event.obj.from_id,
                                                    'balance': 5000,
                                                    'player_id': None,
                                                    'player_name': None
                                                    }
                msg_output = 'Добавлен игрок'

            elif len(parameters) == 1:
                players[str(event.obj.from_id)] = { 'vk_id': event.obj.from_id,
                                                    'balance': 0,
                                                    'player_id': int(parameters[0]),
                                                    'player_name': analyzer.get_player_name(int(parameters[0]))
                                                    }
                msg_output = 'Добавлен игрок с dotaId={}'.format(parameters[0])
            else:
                msg_output = 'Дохуя параметров'

            # сохранение нового списка на сервере
            with open('../data/players.json', 'w', encoding='utf-8', ) as plr:
                json.dump(players, plr, indent=4)

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=msg_output,
            random_id=get_random_id()
        )

    elif event.obj.text.casefold() == '!mystat' or event.obj.text.casefold() == '! mystat':

        # передача в сессию айди хозяина сообщения
        sessions[str(int(event.obj.peer_id))]['player_id'] = players[str(event.obj.from_id)]['player_id']

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='Считанный id: ' + str(sessions[str(event.obj.peer_id)]['player_id']) + ' игрока ' +
                    players[str(event.obj.from_id)]['player_name'],
            random_id=get_random_id()
        )

    elif event.obj.text.casefold() == '!save' or event.obj.casefold == '! save':

        # принудительное сохранение текущего списка игроков
        with open('../data/players.json', 'w', encoding='utf-8', ) as ply:
            ply.write(json.dumps(players, indent=4))

        # принудительное сохранение текущих сессий вместе со значениями
        with open('../data/sessions.json', 'w', encoding='utf-8', ) as ses:
            ses.write(json.dumps(sessions, indent=4))

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='Успешно!',
            random_id=get_random_id()
        )

    elif '!more' in event.obj.text.casefold() or '! more' in event.obj.text.casefold():

        # получение номера искомой позиции в списке
        current_number, error = analyzer.get_parameters_from_text(event.obj.text, param_num=1)

        # проверка на ошибки
        if error:

            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Использование: !more -num',
                random_id=get_random_id()
            )

        else:

            current_number = int(current_number[0][0])

            # Анализ игрока:

            # если сейчас открыт список игроков
            if sessions[str(event.obj.peer_id)]['current_flags']['players']:

                sessions[str(event.obj.peer_id)]['player_id'] = sessions[str(event.obj.peer_id)][
                    'current_player_ids'][current_number - 1]
                try:
                    output = analyzer.get_last_matches(str(sessions[str(event.obj.peer_id)]['player_id']))
                    sessions[str(event.obj.peer_id)]['current_match_ids'] = output[1]
                    output = output[0]

                    player_name = analyzer.get_player_name(sessions[str(event.obj.peer_id)]['player_id'])

                    # свич флагов
                    sessions[str(event.obj.peer_id)]['current_flags']['matches'] = True
                    sessions[str(event.obj.peer_id)]['current_flags']['players'] = False

                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message=player_name,
                        random_id=get_random_id()
                    )

                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message=output,
                        random_id=get_random_id()
                    )
                except:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message='Что-то пошло не так...',
                        random_id=get_random_id()
                    )

            # Анализ матча

            elif sessions[str(event.obj.peer_id)]['current_flags']['matches']:

                # свич флагов
                sessions[str(event.obj.peer_id)]['current_flags']['matches'] = False
                sessions[str(event.obj.peer_id)]['current_flags']['players'] = True

                sessions[str(event.obj.peer_id)]['match_id'] = sessions[str(event.obj.peer_id)][
                    'current_match_ids'][current_number - 1]
                output = analyzer.get_match_information(sessions[str(event.obj.peer_id)]['match_id'])
                sessions[str(event.obj.peer_id)]['current_player_ids'] = output[1]
                output = output[0]

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message=output,
                    random_id=get_random_id()
                )

    elif event.obj.text.casefold() == '!next' or event.obj.text.casefold() == '! next':
        if sessions[str(event.obj.peer_id)]['current_flags']['matches']:
            sessions[str(event.obj.peer_id)]['matches_page'] += 1
            send_last_matches(sessions[str(event.obj.peer_id)]['player_id'], sessions[str(event.obj.peer_id)]['matches_page'])

    elif event.obj.text.casefold() == '!prev' or event.obj.text.casefold() == '! prev':
        if sessions[str(event.obj.peer_id)]['current_flags']['matches'] \
                and sessions[str(event.obj.peer_id)]['matches_page'] != 0:
            sessions[str(event.obj.peer_id)]['matches_page'] -= 1
            send_last_matches(sessions[str(event.obj.peer_id)]['player_id'], sessions[str(event.obj.peer_id)]['matches_page'])

    elif '!invoke' in event.obj.text.casefold() or '! invoke' in event.obj.text.casefold():
        parameters = analyzer.get_parameters_from_text(event.obj.text)[0]
        if not sessions[str(event.obj.peer_id)]['current_flags']['invoke']:
            invoker.invoke(event, vk, longpoll, sessions, parameters)
        else:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Invoker trainer is already on!',
                random_id=get_random_id()
            )
