import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import config as cnfg
from func_database import*
from func_requests import*

#access_token = input('Введите Token: ')
#user_id = input('Введите User_id:')


MIN_SEARCH_AGE = 18
MAX_SEARCH_AGE = 100
RELATION = 6


def write_message(user_id, message):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7)
    })

def find_matches(clients_gender, age, city):
                    relation_profile = RELATION
                    city_profile = city
                    age_profile =  age
                    if clients_gender == 1:
                        gender_profile = 2
                    else:
                        gender_profile = 1
            
                    search_users(gender_profile, relation_profile, age_profile, city_profile)

vk = vk_api.VkApi(token=cnfg.token)
longpoll = VkLongPoll(vk)
started = False
age = 0

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

            message = event.text
            user_id = event.user_id
            
            if message == 'start':
                bdate, city, relation, clients_gender, username  = get_user_data(user_id)
                write_message(event.user_id, f'Привет, {username}!')
                if clients_gender == 0:
                    write_message(event.user_id, 'Заполните в профиле свой пол')
                    write_message(event.user_id, 'После заполнения профиля снова наберите start')
                if city == 0:
                    write_message(event.user_id, 'Заполните в профиле свой город')
                    write_message(event.user_id, 'После заполнения профиля снова наберите start')
                else:                    
                    write_message(user_id, 'Введите примерный возраст поиска командой age:<возраст>, например age:25')
                started = True
            elif message[0:3] == 'age':
                input_age = int(message[4:])
                if input_age < MIN_SEARCH_AGE or input_age > MAX_SEARCH_AGE:
                    write_message(user_id, 'Введите возраст от ' + str(MIN_SEARCH_AGE) + ' до ' + str(MAX_SEARCH_AGE))
                else: 
                    age = input_age
            elif message == 'end':
                write_message(event.user_id, 'Пока!')
            else:
                write_message(event.user_id, 'для начала наберите start\nДля окончания наберите end\nУдачи в поиске')
            
            if started and city != 0 and clients_gender != 0 and age != 0:
                 # добавить @ условие на заполнение всех полей
                find_matches(clients_gender, age, city)
                



#get_user_data(56644)
