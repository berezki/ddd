import json
from vk_api.utils import get_random_id
import datetime
import yaml
from . import analyzer


def seppuku_and_rebirth():
    return 1/0


def admin_check(event, vk, config, players):
    shud_update = False
    if event.obj.from_id in config['admin_ids']:

        if event.obj.text.casefold() == '!config' or event.obj.text.casefold() == '! config':
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message=yaml.dump(config),
                random_id=get_random_id()
            )

        elif event.obj.text.casefold() == '!reboot' or event.obj.text.casefold() == '! reboot':
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Rebooting...',
                random_id=get_random_id()
            )
            seppuku_and_rebirth()

        elif event.obj.text.casefold() == '!troll_mod' or event.obj.text.casefold() == '! troll_mod':
            if config['troll_mod']:
                config['troll_mod'] = False
                stat = 'off'
            else:
                config['troll_mod'] = True
                stat = 'on'

            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Troll mod is {}'.format(stat),
                random_id=get_random_id()
            )
            shud_update = True

        elif event.obj.text.casefold() == '!safe_mod' or event.obj.text.casefold() == '! safe_mod':
            if config['safe_mod']:
                config['safe_mod'] = False
                stat = 'off'
            else:
                config['safe_mod'] = True
                stat = 'on'

            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Safe mod is {}'.format(stat),
                random_id=get_random_id()
            )
            shud_update = True

        elif event.obj.text.casefold() == '!dota_mod' or event.obj.text.casefold() == '! dota_mod':
            if config['dota_mod']:
                config['dota_mod'] = False
                stat = 'off'
            else:
                config['dota_mod'] = True
                stat = 'on'

            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Dota mod is {}'.format(stat),
                random_id=get_random_id()
            )
            shud_update = True

        elif event.obj.text.casefold() == '!pizda_mod' or event.obj.text.casefold() == '! pizda_mod':
            if config['pizda_mod']:
                config['pizda_mod'] = False
                stat = 'disabled'
            else:
                config['pizda_mod'] = True
                stat = 'enabled'
            
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message='Pizda pics are {}'.format(stat),
                random_id=get_random_id()
            )
            shud_update = True

        elif '!setbalance' in event.obj.text.casefold() or '! setbalance' in event.obj.text.casefold():
            params, error = analyzer.get_parameters_from_text(event.obj.text, param_num=1)

            if not error:
                try:
                    i = event.obj.text.casefold().rfind('[')
                    j = event.obj.text.casefold().rfind('|')
                    user_id = event.obj.text.casefold()[i+3:j]
                    sum = int(params[0])
                    players[user_id]
                except KeyError:
                    error = True
            if not error:
                players[user_id]['balance'] = sum
                vk.messages.send(
                    peer_id=event.obj.peer_id,
                    message='Успешно',
                    random_id=get_random_id()
                )
                shud_update = True

    if shud_update:
        with open('data/config.json', 'w', encoding='utf-8', ) as cfg:
            cfg.write(json.dumps(config, indent=4))
        with open('data/players.json', 'w', encoding='utf-8', ) as plr:
            plr.write(json.dumps(players, indent=4))

    return config, players


def send_report(error, config, vk):
   
    now = datetime.datetime.now()

    message = '{}\n{}\n\n'.format(now.strftime('%Y-%m-%d %H:%M:%S'), error)

    with open('output/errors.txt', 'a', encoding='utf-8') as out:
        out.write(message)

    for peer_id in config['admin_ids']:
        vk.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=get_random_id()
        )
