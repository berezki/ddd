import random
from ddd_modules import analyzer
from vk_api.utils import get_random_id

flip_cases = ['Орел', 'Решка']
dhelp = 'Список команд аналайзера:\n' \
        '!newplayer - добавить или изменить информацию о себе\n' \
        '!newsession - создать или обнулить сессию аналайзера для текущей беседы\n' \
        '!session - получить текущую сессию аналайзера\n' \
        '!matches - получить последние 10 матчей (-match_id/-mystat)\n' \
        '!match_ - ввести id матча (-match_id)\n' \
        '!player - ввести id игрока (-player_id)\n' \
        '!mystat - ввести свой id (добавляется командой !newplayer)\n' \
        '!mmr - получить оценочный ммр аккаунта (-player_id/-mystat)\n' \
        '!invoke - запустить инвокер-тренеровщика (-nopic/-notext/-amount)\n' \
        'Некоторые команды могут не работать в Вашей беседе.'

help =  '!flip - подбросить монетку\n' \
        '!roll - получить случайное число (-min -max/ -max)\n' \
        'Некоторые команды могут не работать в Вашей беседе.'


def command_check(event, vk):
    rand_state, rare_message = random.choices([True, False], weights=(1, 100), k=2)

    if rand_state and not rare_message:
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=random.choice(['Подтверждаю', 'Опровергаю']),
            random_id=get_random_id()
        )
    
    elif rand_state and rare_message:
        sex = vk.users.get(user_ids=event.obj.from_id, fields='sex')[0]['sex']
        if sex == 1:  # женский
            message = 'Ты сама поняла что сказала?'
        elif sex == 2:  #мужской
            message = 'Ты сам понял что сказал?'

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=message,
            random_id=get_random_id()
        )

    if event.obj.text.casefold() == '!пинг' or event.obj.text.casefold() == '! пинг':
        ping_output = vk.messages.getConversationMembers(peer_id=event.obj.peer_id)
        conference_ids = []
        i = 0
        j = 0

        while True:
            try:
                if int(ping_output['profiles'][i]['id']) == int(event.obj.from_id):
                    i += 1
                else:
                    conference_ids.append('')
                    conference_ids[j] = ' [id{}|{}]'.format(ping_output['profiles'][i]['id'], ping_output['profiles'][i]['first_name'])
                    i += 1
                    j += 1

            except KeyError:
                break

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=conference_ids,
            random_id=get_random_id()
        )

    elif event.obj.text.casefold() == '!flip' or event.obj.text.casefold() == '! flip':
        
        user = vk.users.get(user_ids=event.obj.from_id, fields='sex')[0]
        if user['sex'] == 1:  # женский
            message = '{} подбросила монетку: {}'.format(user['first_name'], random.choice(flip_cases))
        elif user['sex'] == 2:  # мужской
            message = '{} подбросил монетку: {}'.format(user['first_name'], random.choice(flip_cases))
        
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=message,
            random_id=get_random_id()
        )

    elif '!roll' in event.obj.text.casefold() or '! roll' in event.obj.text.casefold():
        parameters = analyzer.get_parameters_from_text(event.obj.text)[0]
        
        if len(parameters) == 0:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='{} нароллил {}'.format(vk.users.get(user_ids=event.obj.from_id)[0]['first_name'], str(random.randint(1, 100))),
                random_id=get_random_id()
            )

        elif len(parameters) == 1:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message=vk.users.get(user_ids=event.obj.from_id)[0]['first_name'] + ' нароллил ' + str(
                    random.randint(1, int(parameters[0]))),
                random_id=get_random_id()
            )

        elif len(parameters) == 2:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message=vk.users.get(user_ids=event.obj.from_id)[0]['first_name'] + ' нароллил ' + str(
                    random.randint(int(parameters[0]), int(parameters[1]))),
                random_id=get_random_id()
            )
            
    elif event.obj.text.casefold() == 'подтверди или опровергни':
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=random.choice(['Подтверждаю', 'Опровергаю']),
            random_id=get_random_id()
        )
            
    elif 'подтверди' in event.obj.text.casefold():
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='Подтверждаю',
            random_id=get_random_id()
        )
        
    elif 'опровергни' in event.obj.text.casefold():
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='Опровергаю',
            random_id=get_random_id()
        )
    
    elif 'осуди' in event.obj.text.casefold():
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='Опровергаю',
            random_id=get_random_id()
        )

    elif event.obj.text.casefold() == '!help' or event.obj.text.casefold() == '! help':
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=help,
            random_id=get_random_id()
        )
    
    elif event.obj.text.casefold() == '!dhelp' or event.obj.text.casefold() == '! dhelp':
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=dhelp,
            random_id=get_random_id()
        )
    