from ddd_modules import admin, analyzer, casino, commands,dota, invoker, tamagochi, troll
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEventType
from requests import exceptions
import vk_api
import threading
import traceback
import json


class Config:
    def __init__(self):
        self.casino_on = False


def main():

    with open('data/sessions.json', encoding='utf-8') as ses:
        sessions = json.load(ses)

    with open('data/players.json', encoding='utf-8') as ply:
        players = json.load(ply)

    with open('data/config.json', encoding='utf-8') as cfg:
        config = json.load(cfg)

        if config['remember_token']:
            token = config['token']
        else:
            token = input("Enter your group token: ")

        vk_session = vk_api.VkApi(token=token, api_version='5.104')
        vk = vk_session.get_api()
        longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, 189784956)

        print('ddd is on!')

        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW or event.type == VkBotEventType.MESSAGE_REPLY:

                    config, players = admin.admin_check(event, vk, config, players)

                    if (event.obj.from_id in config['admin_ids']) ** config['safe_mod']:
                        
                        commands.command_check(event, vk)

                        if config['troll_mod']:
                            troll.trollCheck(event, vk, config)

                        if config['dota_mod']:
                            dota.dota_check(event, vk, sessions, players, longpoll)

                        if config['casino_mod']:
                            players, sessions = casino.casino_check(event, vk, players, config, sessions)

                        tamagochi.tamagochi_check(event, vk)

        except exceptions.Timeout:
            pass
        except exceptions.ConnectionError:
            pass
        except:
            admin.send_report(traceback.format_exc(), config, vk)
        finally:
            main()


if __name__ == '__main__':
    tmain = threading.Thread(target=main)
    tmain.start()
    tmain.join()
