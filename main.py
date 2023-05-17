import bs4 as bs4
import requests

import datetime

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

# from baza import insert_data_users, creating_database
# from baza import creating_database
# from baza import creating_database, insert_data_users, insert_data_seen_users
# from baza import select
# from baza import insert_data_users
# from baza import insert_data_seen_users
# from baza import insert_data_users
from config import comunity_token, access_token
from config import *



print("Бот запущен")


# def insert_data_users(first_name, last_name, vk_id, vk_link):
#     pass


class Bot_interface:
    def __init__(self, comunity_token, user_id=None):
        # self.longpoll = None
        self.bot = vk_api.VkApi(token=comunity_token)

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        # name = self._USERNAME

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]



    def write_msg(self, user_id, message=None, attachment=None):
        self.bot.method('messages.send', {'user_id': user_id,
                                    'attachment': attachment,
                                    'message': message,
                                    'random_id': get_random_id(), })



    def name(self, user_id):
        """ПОЛУЧЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ НАПИСАЛ БОТУ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': access_token,
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for i in information_dict:
                for key, value in i.items():
                    first_name = i.get('first_name')
                    return first_name
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_sex(self, user_id):
        """ПОЛУЧЕНИЕ ПОЛА ПОЛЬЗОВАТЕЛЯ, МЕНЯЕТ НА ПРОТИВОПОЛОЖНЫЙ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': access_token,
                  'user_ids': user_id,
                  'fields': 'sex',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                if i.get('sex') == 2:
                    find_sex = 1
                    return find_sex
                elif i.get('sex') == 1:
                    find_sex = 2
                    return find_sex
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_age_low(self, user_id):
        """ПОЛУЧЕНИЕ ВОЗРАСТА ПОЛЬЗОВАТЕЛЯ ИЛИ НИЖНЕЙ ГРАНИЦЫ ДЛЯ ПОИСКА"""
        url = url = f'https://api.vk.com/method/users.get'
        params = {'access_token': access_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                date = i.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
            elif len(date_list) == 2 or date not in information_list:
                self.write_msg(user_id, 'Введите нижний порог возраста (min - 16): ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_age_high(self, user_id):
        """ПОЛУЧЕНИЕ ВОЗРАСТА ПОЛЬЗОВАТЕЛЯ ИЛИ ВЕРХНЕЙ ГРАНИЦЫ ДЛЯ ПОИСКА"""
        url = url = f'https://api.vk.com/method/users.get'
        params = {'access_token': access_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                date = i.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
            elif len(date_list) == 2 or date not in information_list:
                self.write_msg(user_id, 'Введите верхний порог возраста (max - 65): ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    # @staticmethod
    def cities(self, user_id, city_name):
        """ПОЛУЧЕНИЕ ID ГОРОДА ПОЛЬЗОВАТЕЛЯ ПО НАЗВАНИЮ"""
        url = url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': access_token,
                  'country_id': 1,
                  'q': f'{city_name}',
                  'need_all': 0,
                  'count': 1000,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            list_cities = information_list['items']
            for i in list_cities:
                found_city_name = i.get('title')
                if found_city_name == city_name:
                    found_city_id = i.get('id')
                    return int(found_city_id)
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_city(self, user_id):
        """ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ГОРОДЕ ПОЛЬЗОВАТЕЛЯ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': access_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for i in information_dict:
                if 'city' in i:
                    city = i.get('city')
                    id = str(city.get('id'))
                    return id
                elif 'city' not in i:
                    self.write_msg(user_id, 'Введите название вашего города: ')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city_name = event.text
                            id_city = self.cities(user_id, city_name)
                            if id_city != '' or id_city != None:
                                return str(id_city)
                            else:
                                break
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_user(self, user_id):
        """ПОИСК ЧЕЛОВЕКА ПО ПОЛУЧЕННЫМ ДАННЫМ"""
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': access_token,
                  'v': '5.131',
                  'sex': self.get_sex(user_id),
                  'age_from': self.get_age_low(user_id),
                  'age_to': self.get_age_high(user_id),
                  'city': self.find_city(user_id),
                  'fields': 'is_closed, id, first_name, last_name',
                  'status': '1' or '6',
                  'count': 500}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        try:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
            for person_dict in list_1:
                if person_dict.get('is_closed') == False:
                    first_name = person_dict.get('first_name')
                    last_name = person_dict.get('last_name')
                    vk_id = str(person_dict.get('id'))
                    vk_link = 'vk.com/id' + str(person_dict.get('id'))
                    insert_data_users(first_name, last_name, vk_id, vk_link)
                else:
                    continue
            return f'Поиск завершён'
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photos_id(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИЙ С РАНЖИРОВАНИЕМ В ОБРАТНОМ ПОРЯДКЕ"""
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': access_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.131'}
        resp = requests.get(url, params=params)
        dict_photos = dict()
        resp_json = resp.json()
        try:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
            for i in list_1:
                photo_id = str(i.get('id'))
                i_likes = i.get('likes')
                if i_likes.get('count'):
                    likes = i_likes.get('count')
                    dict_photos[likes] = photo_id
            list_of_ids = sorted(dict_photos.items(), reverse=True)
            return list_of_ids
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photo_1(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ № 1"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 1:
                return i[1]

    def get_photo_2(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ № 2"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 2:
                return i[1]

    def get_photo_3(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ № 3"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 3:
                return i[1]

    def send_photo_1(self, user_id, message, offset):
        """ОТПРАВКА ПЕРВОЙ ФОТОГРАФИИ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': access_token,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(offset)}_{self.get_photo_1(self.person_id(offset))}',
                                         'random_id': 0})

    def send_photo_2(self, user_id, message, offset):
        """ОТПРАВКА ВТОРОЙ ФОТОГРАФИИ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': access_token,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(offset)}_{self.get_photo_2(self.person_id(offset))}',
                                         'random_id': 0})

    def send_photo_3(self, user_id, message, offset):
        """ОТПРАВКА ТРЕТЬЕЙ ФОТОГРАФИИ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': access_token,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(offset)}_{self.get_photo_3(self.person_id(offset))}',
                                         'random_id': 0})

    def find_persons(self, user_id, offset):
        self.write_msg(user_id, self.found_person_info(offset))
        self.person_id(offset)
        insert_data_seen_users(self.person_id(offset), offset)  # offset
        self.get_photos_id(self.person_id(offset))
        self.send_photo_1(user_id, 'Фото номер 1', offset)
        if self.get_photo_2(self.person_id(offset)) != None:
            self.send_photo_2(user_id, 'Фото номер 2', offset)
            self.send_photo_3(user_id, 'Фото номер 3', offset)
        else:
            self.write_msg(user_id, f'Больше фотографий нет')

    def found_person_info(self, offset):
        """ВЫВОД ИНФОРМАЦИИ О НАЙДЕННОМ ПОЛЬЗОВАТЕЛИ"""
        tuple_person = select(offset)
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return f'{list_person[0]} {list_person[1]}, ссылка - {list_person[3]}'

    def person_id(self, offset):
        """ВЫВОД ID НАЙДЕННОГО ПОЛЬЗОВАТЕЛЯ"""
        tuple_person = select(offset)
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return str(list_person[2])

    # API-ключ созданный ранее
# token = "vk1.a.dkpVykCwLT6jOXK2i3Ujnwrou8HbU6-eBMODsFRzJJHlTd-13tZJeEccuDHr3HNLvwY510S3OmJ4O6WajOJ1-m06Njy_cpz5kMxp_FYvhAwbN9GY4qMugkM9Vb5HFxHIbI5QYGv4RbmZwjH2EIfJS6xVC6IKxQMPoB1gzYTKMnI4qjWa--te9sQPQdGXuK5_EwXNiKV3gvx0tEBIIpgFTg"


#   # Авторизуемся как сообщество
# vk = vk_api.VkApi(token=token)
#
#   # Работа с сообщениями
# longpoll = VkLongPoll(vk)

# Commander
# commander = Commander()



# эхо / это называется эхо, бот типо повторяет и возвращает ответ. Мдааа, ну это больше похоже на РЕВЕРБЕРАЦИЮ
    def handler(self, offset=None):
        longpoll = VkLongPoll(self.bot)

        # Основной цикл
        for event in longpoll.listen():

            # Если пришло новое сообщение
            if event.type == VkEventType.MESSAGE_NEW:

                # Если оно имеет метку для меня( то есть бота)
                if event.to_me:
                    print(f'Сообщение от {event.user_id}', end='\n')
                    print('Вот текст:', event.text)

                    # Сообщение от пользователя
                    request = event.text.lower() # Запрос
                    send = self.write_msg # Отправить сообщение. Писать или так или так.

                    # creating_database()
                    # bot.write_msg(user_id, f'Привет, {bot.name(user_id)}')
                    # bot.find_user(user_id)
                    # bot.write_msg(event.user_id, f'Нашёл для тебя пару, жми на кнопку "Вперёд"')
                    # bot.find_persons(user_id, offset)
                    user_id = event.user_id


                    # Логика ответа
                    if request == "привет" or request == 'ghbdtn':
                        send(user_id,f'{bot.name(user_id)}, привет чудило! &#128524;')


                    elif request == "здорово" or request == 'здарово':
                        send(user_id,f'{bot.name(user_id)}, здарово, здарово чудило! &#128527;')


                    elif request == "пришли клоуна" or request == 'клоун':
                        # send(user_id, f'{bot.name(user_id)}, здарово, здарово чудило! &#128527;')
                        fotka = 'photo379597632_457240030'
                        send(user_id, f'Вот:', attachment=fotka)



                    elif request == 'начать поиск' or request == 'начать' or request == 'поиск':

                        creating_database()

                        bot.write_msg(user_id, f'Ну чё, {bot.name(user_id)}?')
                        bot.find_user(user_id)
                        bot.write_msg(user_id, f'Нашёл для тебя пару, пиши слово "Вперёд"')
                        bot.find_persons(user_id, offset)

                    elif request == 'вперёд':
                        for i in line:
                            offset += 1
                            bot.find_persons(user_id, offset)
                            break

                    # else:
                    #     bot.write_msg(event.user_id, 'Твоё сообщение непонятно')




                    elif request == "как ты" or request == 'как дела':
                        send(user_id, f"Отлично! А как у тебя, {bot.name(user_id)}, если честно, мне наплевать;))) ")
                    elif request == "как ты?" or request == 'как дела?':
                        send(user_id, f"Отлично! А как у тебя, {bot.name(user_id)}, если честно, мне наплевать;))) ")



                    elif request == "пока" or request == 'вали':
                        send(user_id, f'Пока, {bot.name(user_id)}, пока.')


                    else:
                        self.write_msg(user_id, f"Ты, {bot.name(user_id)}, херню несёшь! &#128580;")


    def _clean_all_tag_from_str(self, string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result





if __name__ == '__main__':
    bot = Bot_interface(comunity_token)
    # fotka = 'photo379597632_457240030' # Моя фотка с табличкой
    # fotka = 'https://sun9-75.userapi.com/impg/tjQSud087nOJlYPocWIkcerAbjpruQkTxmKyTw/DcQ0qLlFh88.jpg?size=1280x853&quality=95&sign=5608305645178929ca558a6c4336fdde&type=album' # Моя фотка с табличкой
    fotka = "photo-219866043_457239212"
    bot.write_msg(765953848, f'Здарово!!! Я бот.\nТы можешь спросить у меня как я, как дела. И помутить тёлочек, если ты пацан. ', attachment = fotka)

    bot.handler()