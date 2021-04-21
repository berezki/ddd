from pydantic import BaseModel
import json
from ddd_modules.analyzer import get_parameters_from_text
from datetime import datetime

class Good(BaseModel):

    id: int
    name: str
    value: int
    fun: int
    price: int
    

class Pet(BaseModel):

    id: int
    name: str
    bellyful: int
    mood: int
    cleanness: int
    last_time: datetime
    goods: list[Good]

    def update_pet(self, current_time=datetime.now()):
        hours_passed = (current_time - self.last_time).seconds // (60 * 60)
        self.bellyful -= hours_passed
        self.mood -= hours_passed
        self.cleanness -= hours_passed
        self.last_time = current_time

    def eat(self, food: Good):
        self.bellyful += food.value
        if self.bellyful > 15:
            self.bellyful = 15

    def play(self, toy: Good):
        self.mood += toy.fun
        if self.mood > 15:
            self.mood = 15

    def wash(self):
        self.cleanness = 0


with open('data/pets.json', encoding='utf-8') as pts:
    pets = {}
    pets_obj = json.load(pts)
    for user in pets_obj:
        pets[user] = Pet(**pets_obj[user])

with open('data/goods.json', encoding='utf-8') as gds:
    goods = {}
    goods_obj = json.load(gds)
    for good in goods_obj:
        goods[good] = Good(**goods_obj[good])


def tamagochi_check(event, vk):

    if '!rename' in event.obj.text.casefold() or '! rename' in event.obj.text.casefold():
        new_name, error = get_parameters_from_text(event.obj.text.casefold(), 1)
        if not error:
            pets[str(event.obj.from_id)].name = new_name[0]
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message="Теперь твоего питомца зовут {}!".format(pets[str(event.obj.from_id)].name),
                random_id=0
            )
        else:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message="Нормально имя введи",
                random_id=0
            )

    elif event.obj.text.casefold() == '!play' or event.obj.text.casefold() == '! play':
        pets[str(event.obj.from_id)].play(goods['straw_icecream'])
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message="Твой питомец поиграл",
            random_id=0
        )

    elif event.obj.text.casefold() == '!eat' or event.obj.text.casefold() == '! eat':
        pets[str(event.obj.from_id)].eat(goods['straw_icecream'])
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message="Твой питомец поел",
            random_id=0
        )

    elif event.obj.text.casefold() == '!stats' or event.obj.text.casefold() == '! stats':
        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=str(pets[str(event.obj.from_id)]),
            random_id=0
        )

    elif event.obj.text.casefold() == '!shop' or event.obj.text.casefold() == '! shop':
        master_str = ""
        for good in goods:
            master_str += "{} - {} танго\n".format(goods[good].name, goods[good].price)

        vk.messages.send(
            peer_id=event.obj.peer_id,
            message=master_str,
            random_id=0
        )
