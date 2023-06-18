from datetime import datetime
from random import randrange

from vk_api import VkTools, keyboard
from vk_api.utils import get_random_id

from config import *
from db import *

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk = vk_api.VkApi(token=comm_token)
longpoll = VkLongPoll(vk)

class VkBot():
    def __init__(self, comm_token, user_token):
        self.vk = vk_api.VkApi(token=comm_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(user_token)
        self.params = {}
        self.worksheets = []
        self.offset = 0


    def message_send(self, user_id, message, attachment=None):
        vk.method('messages.send', {'user_id': user_id,
                                    'message': message,
                                    'attachment': attachment,
                                    'random_id': get_random_id()})

    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    if self.params is not None:
                        if not self.params['city']:
                            self.message_send(event.user_id, f'Привет, {self.params["name"]}, введите название вашего '
                                                             'города проживания:', keyboard=keyboard.get_keyboard())
                            while True:
                                for event_ in self.longpoll.listen():
                                    if event_.type == VkEventType.MESSAGE_NEW and event_.to_me:
                                        self.params['city'] = event_.text
                                        break
                        elif not self.params['sex']:
                            self.message_send(event.user_id, 'Введите ваш пол:', keyboard=keyboard.get_keyboard())
                            self.params['sex'] = 2 if event.text == 'Мужской' else 1
                            while True:
                                for event_ in self.longpoll.listen():
                                    if event_.type == VkEventType.MESSAGE_NEW and event_.to_me:
                                        self.params['sex'] = event_.text
                                        break
                        elif not self.params['year']:
                            self.message_send(event.user_id, 'Введите ваш возраст:', keyboard=keyboard.get_keyboard())
                            self.params['year'] = event.text
                            while True:
                                for event_ in self.longpoll.listen():
                                    if event_.type == VkEventType.MESSAGE_NEW and event_.to_me:
                                        self.params['year'] = event_.text
                                        break
                        elif not self.params['relation'] or self.params['relation'] is None:
                            self.message_send(event.user_id, 'Введите ваши отношении:',
                                              keyboard=keyboard.get_keyboard())
                            self.params['relation'] = event.text
                            while True:
                                for event_ in self.longpoll.listen():
                                    if event_.type == VkEventType.MESSAGE_NEW and event_.to_me:
                                        self.params['relation'] = event_.text
                                        break
                        else:
                            self.message_send(event.user_id, f'Привет, {self.params["name"]}, напиши "Поиск", '
        'чтобы найти анкеты', keyboard=keyboard.get_keyboard())
                    else:
                        self.message_send(event.user_id, 'Ошибка получения данных', keyboard=keyboard.get_keyboard())


                elif event.text.lower() == 'поиск':
                    self.message_send(event.user_id, 'Начинаем поиск')
                    if self.worksheets:
                        worksheet = self.worksheets.pop()
                        photos=self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_photo["id"],'
                    else:
                        self.worksheets = self.vk_tools.search_worksheet(self.params, self.offset)
                        worksheet = self.worksheets.pop()
                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_photo["id"],'
                        self.offset += 10

                        self.message_send(
                            event.user_id,
                            f'Имя: {worksheet["name"]} Cсылка: vk.com/{worksheet["id"]}',
                            attachment=photo_string
                        )

                elif event.text.lower() == 'пока':
                    self.message_send(event.user_id, 'Пока!')
                else:
                    self.message_send(event.user_id, 'Не понял тебя')


vk = vk_api.VkApi(token=comm_token)
longpoll = VkLongPoll(vk)

if __name__ == '__main__':
    bot_interface = VkBot(comm_token, user_token)
    bot_interface.event_handler()