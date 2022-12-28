import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import config as cnfg
from func_database import*
from func_requests import*

#access_token = input('Введите Token: ')

search_users
MIN_SEARCH_AGE = 18
MAX_SEARCH_AGE = 100
RELATION = 6
NEW_PROFILE_STATUS = 'new'
user_id: int

def write_message(user_id, message):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7)
    })


def send_photo(user_id, candidate_id, photo_id):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': '',
        'attachment': 'photo{}_{}'.format(candidate_id, photo_id),
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

    ids_profile_list = search_users(gender_profile, age_profile, city_profile, relation_profile)
    add_client(user_id, ids_profile_list, NEW_PROFILE_STATUS)


def show_one_profile():
    candidate_id = get_next_profile(user_id)
    candidate_url = 'https://vk.com/id' + str(candidate_id)
    write_message(user_id, candidate_url)   
    photo_urls = get_photos(candidate_id)
    for i in range(min(3, len(photo_urls))):
        send_photo(user_id, candidate_id, photo_urls[i])
    mark_as_shown(user_id, candidate_id)

vk = vk_api.VkApi(token=cnfg.token)
longpoll = VkLongPoll(vk)
started = False
show_next = False
age = 0


def message_manager():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

                message = event.text
                user_id = event.user_id
                
                if message == 'start':
                    bdate, city, relation, clients_gender, username  = get_user_data(user_id)
                    write_message(user_id, f'Привет, {username}!')
                    if clients_gender == 0:
                        write_message(user_id, 'Заполните в профиле свой пол')
                        write_message(user_id, 'После заполнения профиля снова наберите start')
                    if city == 0:
                        write_message(user_id, 'Заполните в профиле свой город')
                        write_message(user_id, 'После заполнения профиля снова наберите start')
                    else:                    
                        write_message(user_id, 'Введите примерный возраст поиска командой age:<возраст>, например age:25')
                    started = True
                    #age = 30 #убрать это, раскомментировать следующую секцию
                elif message[0:3] == 'age':
                    input_age = int(message[4:])
                    if input_age < MIN_SEARCH_AGE or input_age > MAX_SEARCH_AGE:
                        write_message(user_id, 'Введите возраст от ' + str(MIN_SEARCH_AGE) + ' до ' + str(MAX_SEARCH_AGE))
                    else: 
                        age = input_age
                elif message == 'next':
                    show_next = True
                elif message == 'end':
                    write_message(user_id, 'Пока!')
                    close_db()
                    quit()                
                else:
                    write_message(user_id, 'Для начала наберите start\nДля окончания наберите end\nУдачи в поиске')
                
                if started and city != 0 and clients_gender != 0 and age != 0:
                    # добавить @ условие на заполнение всех полей
                    find_matches(clients_gender, age, city)
                    show_next = True
                    started = False

                if show_next:
                    show_one_profile()
                    write_message(user_id, 'Для показа следующей анкеты наберите next. Для окончания наберите end.')

message_manager()