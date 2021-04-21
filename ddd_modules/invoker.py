from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType
import random
import time
import threading

spells_list = [
    {
        'name': 'Cold snap',
        'cast': ['qqq'],
        'icon': 'photo-189784956_457239025'
    },

    {
        'name': 'Ghost walk',
        'cast': ['qqw', 'qwq', 'wqq'],
        'icon': 'photo-189784956_457239029'
    },

    {
        'name': 'Ice wall',
        'cast': ['qqe', 'qeq', 'eqq'],
        'icon': 'photo-189784956_457239030'
    },

    {
        'name': 'Tornado',
        'cast': ['wwq', 'wqw', 'qww'],
        'icon': 'photo-189784956_457239032'
    },

    {
        'name': 'Deafening blast',
        'cast': ['qwe', 'weq', 'eqw', 'ewq', 'wqe', 'qew'],
        'icon': 'photo-189784956_457239026'
    },

    {
        'name': 'Forge spirit',
        'cast': ['eeq', 'eqe', 'qee'],
        'icon': 'photo-189784956_457239028'
    },

    {
        'name': 'EMP',
        'cast': ['www'],
        'icon': 'photo-189784956_457239027'
    },

    {
        'name': 'Alacrity',
        'cast': ['wwe', 'wew', 'eww'],
        'icon': 'photo-189784956_457239023'
    },

    {
        'name': 'Chaos meteor',
        'cast': ['eew', 'ewe', 'wee'],
        'icon': 'photo-189784956_457239024'
    },

    {
        'name': 'Sun strike',
        'cast': ['eee'],
        'icon': 'photo-189784956_457239031'
    }
]


def wait_thread(event, vk, longpoll, sessions, i, sumtime, parameters):
    spell = random.choice(spells_list)
    nopic, notext, amount = parameters
    if not notext:
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='{}/{} {}'.format(i+1, amount, spell['name']),
            random_id=get_random_id()
        )

    if not nopic:
        vk.messages.send(
            peer_id=event.obj.peer_id,
            attachment=spell['icon'],
            random_id=get_random_id()
        )

    i += 1
    event_first = event
    time0 = int(time.time()*100)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW or event.type == VkBotEventType.MESSAGE_REPLY:
            if event.obj.peer_id == event_first.obj.peer_id and event.obj.text.casefold() in spell['cast']:

                time1 = round((int(time.time()*100) - time0)/100, 3)
                sumtime += time1
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Your result is {} seconds'.format(time1),
                    random_id=get_random_id()
                )

                if i != amount:
                    wait_thread(event, vk, longpoll, sessions, i, sumtime, parameters)

                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Your average time is {} seconds, nettime is {} secs'.format(round(sumtime/amount, 2), round(sumtime, 2)),
                    random_id=get_random_id()
                )

                sessions[str(event.obj.peer_id)]['current_flags']['invoke'] = False
                quit()


def invoke(event, vk, longpoll, sessions, parameters):
    nopic = False
    notext = False
    amount = 5

    sessions[str(event.obj.peer_id)]['current_flags']['invoke'] = True

    for i in range(len(parameters)):
        if parameters[i] == 'nopic':
            nopic = True
        elif parameters[i] == 'notext':
            notext = True
        elif parameters[i].isdigit():
            if amount <= 25:
                amount = int(parameters[i])
            else:
                amount = 25

    parameters = [nopic, notext, amount]
    i = 0
    sumtime = 0
    tinvo = threading.Thread(target=wait_thread, args=(event, vk, longpoll, sessions, i, sumtime, parameters))
    tinvo.start()