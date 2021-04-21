import random
from . import analyzer
from vk_api.utils import get_random_id
import time
import threading
import json


class BetPool:
    net = 0
    bets = []
    color = ''


def roulette_roll():
    color = random.choices(['green', 'red', 'black'], weights=(1, 18, 18), k=1)[0]
    BetPool.color = color


def roulette_wins(players, vk):
    winpool = 0
    winbets = []
    losebets = []
    sessions_take_part = []
    j = 0
    while j < len(BetPool.bets):
        if BetPool.bets[j]['peer_id'] not in sessions_take_part:
            sessions_take_part.append(BetPool.bets[j]['peer_id'])
        j += 1

    for peer_id in sessions_take_part:
        vk.messages.send(
            peer_id=peer_id,
            message='На рулетке выпало... {}'.format(BetPool.color),
            random_id=get_random_id()
        )

    i = 0
    while i < len(BetPool.bets):
        if BetPool.bets[i]['color'] == BetPool.color:
            winpool += BetPool.bets[i]['bet_val']
            winbets.append(i)
        if BetPool.bets[i]['color'] != BetPool.color:
            losebets.append(i)
        i += 1

    i = 0
    while i < len(BetPool.bets):
        if i in winbets and winpool != 0:
            winval = round((BetPool.net / winpool) * BetPool.bets[i]['bet_val'])
            add_sum_to_balance(BetPool.bets[i]['from_id'], winval, players)

            vk.messages.send(
                peer_id=BetPool.bets[i]['peer_id'],
                message='{} выиграл ставку и получил '
                        '{} танго на свой счет, поздравим!'.format(
                                                    vk.users.get(user_ids=BetPool.bets[i]['from_id'])[0]['first_name'],
                                                    winval),
                random_id=get_random_id()
            )

        elif i in losebets:
            vk.messages.send(
                peer_id=BetPool.bets[i]['peer_id'],
                message='К сожалению, {} все проиграл, не растраивайся!'.format(
                    vk.users.get(user_ids=BetPool.bets[i]['from_id'])[0]['first_name']
                ),
                random_id=get_random_id()
            )

        i += 1
    BetPool.net = 0
    BetPool.bets = []
    BetPool.color = ''


def add_sum_to_balance(user_id, val, players):
    players[str(user_id)]['balance'] += val
    with open('data/players.json', 'w', encoding='utf-8', ) as plr:
        json.dump(players, plr, indent=4)
    return players


def remove_sum_from_balance(user_id, val, players):
    players[str(user_id)]['balance'] -= val
    with open('data/players.json', 'w', encoding='utf-8', ) as plr:
        json.dump(players, plr, indent=4)
    return players


def timer_casino(min, config, players, vk):
    time.sleep(min*60)
    roulette_roll()
    config['casino_on'] = False
    roulette_wins(players, vk)


def casino_check(event, vk, players, config, sessions):
    error = False
    try:
        players[str(event.obj.from_id)]
    except KeyError:
        error = True
    
    if not error:
        if '!roulette' in event.obj.text.casefold() or '! roulette' in event.obj.text.casefold():

            time, error = analyzer.get_parameters_from_text(event.obj.text, param_num=1)
            if not error:
                time = int(time[0])

                if error:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message="Использование: !roulette -время в минутах на принятие ставок",
                        random_id=get_random_id()
                    )

                else:
                    for chat in sessions:
                        print(chat)
                        print(sessions[chat])
                        if sessions[chat]['current_flags']['casino_notifications_enabled']:
                            vk.messages.send(
                                peer_id=chat,
                                message='Ваши ставки, Господа! Ждем {} минут и начинаем!'.format(time),
                                random_id=get_random_id()
                            )

                    config['casino_on'] = True

                    ttimercasino = threading.Thread(target=timer_casino, args=(time, config, players, vk))
                    ttimercasino.start()
                
        elif '!casino' in event.obj.text.casefold() or '! casino' in event.obj.text.casefold():
            bet, error = analyzer.get_parameters_from_text(event.obj.text, param_num=2)
            try:
                    bet_val = int(bet[0])
                    if bet[1] == 'green' or bet[1] == 'black' or bet[1] == 'red':
                        pass
                    else:
                        error = True
            except:
                error = True
                    
            if error:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message="Использование: !casino -сумма ставки -цвет (black, red, green)",
                        random_id=get_random_id()
                    )
            else:
                if players[str(event.obj.from_id)]['balance'] < bet_val:

                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message="Недостаточно танго",
                        random_id=get_random_id()
                    )

                else:
                    remove_sum_from_balance(event.obj.from_id, bet_val, players)
                    color = random.choices(['green', 'red', 'black'], weights=(1, 18, 18), k=1)[0]
                    if bet[1] == color == 'black' or bet[1] == color == 'red':
                        add_sum_to_balance(event.obj.from_id, bet_val * 2, players)

                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message="Поздравляем, вы выиграли {} танго!".format(bet_val*2),
                            random_id=get_random_id()
                        )
                    elif bet[1] == color == 'green':

                        add_sum_to_balance(event.obj.from_id, bet_val * 14, players)
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message="Поздравляем, вы сорвали куш и выиграли {} танго!".format(bet_val*14),
                            random_id=get_random_id()
                        )

                    else:
                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message="Поздравляем, вы все проиграли!",
                            random_id=get_random_id()
                        )
                    
        elif '!bet' in event.obj.text.casefold() or '! bet' in event.obj.text.casefold():
            if config['casino_on']:
                bet, error = analyzer.get_parameters_from_text(event.obj.text, param_num=2)

                try:
                    bet_val = int(bet[0])
                    if bet[1] == 'green' or bet[1] == 'black' or bet[1] == 'red':
                        pass
                    else:
                        error = True
                except:
                    error = True

                if error:
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message="Использование: !bet -сумма ставки -цвет (black, red, green)",
                        random_id=get_random_id()
                    )

                else:
                    if players[str(event.obj.from_id)]['balance'] < bet_val:

                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message="Недостаточно танго",
                            random_id=get_random_id()
                        )

                    else:
                        remove_sum_from_balance(event.obj.from_id, bet_val, players)
                        BetPool.net += bet_val
                        BetPool.bets.append({
                            'peer_id': event.obj.peer_id,
                            'from_id': event.obj.from_id,
                            'bet_val': int(bet[0]),
                            'color': bet[1]
                        })

                        vk.messages.send(
                            peer_id=event.obj.peer_id,
                            message='{} танго поставлено на {}'.format(bet[0], bet[1]),
                            random_id=get_random_id()
                        )

            else:
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Ставки не принимаются',
                    random_id=get_random_id()
                )

        elif '!pay' in event.obj.text.casefold() or '! pay' in event.obj.text.casefold():
            sum, error = analyzer.get_parameters_from_text(event.obj.text, param_num=1)
        
            i = event.obj.text.casefold().rfind('[')
            j = event.obj.text.casefold().rfind('|')
            user_id = event.obj.text.casefold()[i+3:j]

            try:
                sum = int(sum[0])
                players[str(event.obj.from_id)] # проверка отправителя
                players[str(user_id)]           # проверка получателя
            except:
                error = True

            if not error and (sum > players[str(event.obj.from_id)]['balance']):
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Недостаточно танго',
                    random_id=get_random_id()
                )
                error = True

            if not error:
                players = add_sum_to_balance(user_id, sum, players)
                players = remove_sum_from_balance(event.obj.from_id, sum, players)
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Было успешно отправлено {} танго'.format(sum),
                    random_id=get_random_id()
                )

            else:
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Использование: !pay @user -сумма',
                    random_id=get_random_id()
                )

        elif '!balance' in event.obj.text.casefold() or '! balance' in event.obj.text.casefold():
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='На вашем счету {} танго'.format(players[str(event.obj.from_id)]['balance']),
                random_id=get_random_id()
            )
        
        elif '!дать леща' in event.obj.text.casefold() or '! дать леща' in event.obj.text.casefold():
            error = False
            try:
                i = event.obj.text.casefold().rfind('[')
                j = event.obj.text.casefold().rfind('|')
                user_id = event.obj.text.casefold()[i+3:j]
            except:
                error = True
            if not error and (1000 > players[str(event.obj.from_id)]['balance']):
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Недостаточно танго',
                    random_id=get_random_id()
                )
            elif not error:
                players = remove_sum_from_balance(event.obj.from_id, 1000, players)
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='[id{}|{}] получает смачного леща'.format(
                        user_id,
                        vk.users.get(user_ids=user_id)[0]['first_name']),
                    random_id=get_random_id()
                )

        elif  event.obj.text.casefold() == '!notify' or event.obj.text.casefold() == '! notify':
            if sessions[str(event.obj.peer_id)]['current_flags']['casino_notifications_enabled']:
                sessions[str(event.obj.peer_id)]['current_flags']['casino_notifications_enabled'] = False
                notify_output = 'Уведомления выключены'
            else:
                sessions[str(event.obj.peer_id)]['current_flags']['casino_notifications_enabled'] = True
                notify_output = 'Уведомления включены'
            
            with open('../data/sessions.json', 'w', encoding='utf-8', ) as ses:
                ses.write(json.dumps(sessions, indent=4))
            
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message=notify_output,
                random_id=get_random_id()
            )

    return players, sessions
