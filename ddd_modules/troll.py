import random
from vk_api.utils import get_random_id

dot = ['Солнышко', 'Зайка', 'Лучший', 'Котик', 'Хороший человек']
pizda = ['Cunt', 'Chatte', 'Muschi', 'Песи', 'Мысык']
pizda_pics = ['photo-189784956_457239019', 'photo-189784956_457239034', 'photo-189784956_457239033']

def trollCheck(event, vk, config):

    elif 'крест ' in event.obj.text.casefold() or ' крест' in event.obj.text.casefold() or event.obj.text.casefold() == 'крест':
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='Доминика Торетто',
            random_id=get_random_id()
        )

    elif event.obj.text.casefold() == 'дюшес':
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='ММММММ ГРУШИИ',
            random_id=get_random_id()
        )

    elif event.obj.text.casefold() == 'релиз':
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message="в 2040",
            random_id=get_random_id()
        )


    elif event.obj.text.casefold() == 'да' \
            or event.obj.text.casefold() == 'дa' \
            or event.obj.text.casefold() == 'дa.' \
            or event.obj.text.casefold() == 'да.':
        if config['pizda_mod']:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                attachment=random.choice(pizda_pics),
                random_id=get_random_id()
            )
        else:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message=random.choice(pizda),
                random_id=get_random_id()
            )

    elif event.obj.text.casefold() == 'нет' \
        or event.obj.text.casefold() == 'hет' \
        or event.obj.text.casefold() == 'нeт' \
        or event.obj.text.casefold() == 'нeт' \
        or event.obj.text.casefold() == 'heт':
        
        if event.obj.from_id in config['white_list']:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Солнышка ответ',
                random_id=get_random_id()
            )
        else:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='ответ',
                random_id=get_random_id()
            )
        

    elif event.obj.text.casefold() == 'хто мы':

        conf_output = vk.messages.getConversationMembers(peer_id=event.obj.peer_id)
        conference_ids = []
        i = 0
        j = 0

        while True:
            try:
                name = conf_output['profiles'][i]['first_name'] + ' ' + conf_output['profiles'][i]['last_name']
                conference_ids.append('')
                conference_ids[i] = name
                i += 1

            except:
                break

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='{} {}'.format(random.choice(conference_ids), random.choice(dot)),
            random_id=get_random_id()
        )

    elif event.obj.text.casefold() == 'хто я':

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=random.choice(dot),
            random_id=get_random_id()
        )
            
    elif 'срать' in event.obj.text.casefold():
        vk.messages.send(
            peer_id=event.obj.peer_id,
            attachment='photo-189784956_457239035',
            random_id=get_random_id()
        )
        
    elif event.obj.text.casefold() == 'ага':
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message='В жопе нога',
            random_id=get_random_id()
        )