
from config import access_token
import requests
import time


NUM_READ_PROFILES = 5 #количество запрашиваемых анкет за один поиск
AGE_RANGE = 2


def get_user_data(user_id): 
    URL = 'https://api.vk.com/method/users.get'
    params = {
            'access_token': access_token,
            'v': '5.131', 'fields': 'domain, bdate, city, relation, sex'
            }

    res = requests.get(URL, params=params)
    response = res.json()
    
    username = response['response'][0]['first_name'] + ' ' + response['response'][0]['last_name'] 
    bdate = response['response'][0]['bdate']
    city = response['response'][0]['city']['id']
    relation = response['response'][0]['relation']
    clients_gender = response['response'][0]['sex']
    id = response['response'][0]['id']
    
    return bdate, city, relation, clients_gender, username
       

def search_users(gender_profile, age_profile, city_profile, relation_profile):
    URL = 'https://api.vk.com/method/users.search'
    
    age_from = int(age_profile) - AGE_RANGE
    age_to = int(age_profile) + AGE_RANGE
    print(age_from, age_to)
    params = {
            'access_token': access_token,
            'sex': gender_profile,
            'city': city_profile,
            #'age_from': age_from,
            #'age_to': age_to,
            'relation': relation_profile,
            'offset': 500,
            'count': NUM_READ_PROFILES,
            'v': '5.131', 
            'fields': 'id, bdate, city, relation, status, age_to, sex'
            }

    try:
        res = requests.get(URL, params=params)
        response = res.json()

    except Exception as e:
        print(f'Ошибка запроса: {e}')
        raise SystemExit()
    time.sleep(5)
    
    res = requests.get(URL, params=params)
    response = res.json()
    ids_of_users = response['response']['items']
    ids_profile_list = []

    for i in range(len(ids_of_users)):
        id_profile = ids_of_users[i]['id']
        ids_profile_list.append(id_profile)
    print(ids_profile_list)
    return ids_profile_list


def get_photos(id_profile):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
            'access_token': access_token,
            'owner_id': id_profile,
            'album_id': 'profile',
            'count': 10,
            'v': '5.131', 
            'extended': 1
            }

    res = requests.get(URL, params=params)
    response = res.json()
    photos = response['response']['items']
    photos_likes = []

    for i in range(len(photos)):
        likes = photos[i]['likes']['count'] + photos[i]['comments']['count']
        photos_likes.append([likes,i])

    photos_likes.sort(reverse=True)
    photo_urls = []
    for i in range(min(3, len(photos))):
        photo_id = photos[photos_likes[i][1]]['id']
        photo_urls.append(photo_id)
    return photo_urls
    
    
    
