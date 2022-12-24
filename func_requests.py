import vk_api
from config import access_token
import requests
import time

# vk = vk_api.VkApi(token='access_token')
NUM_READ_PROFILES = 5 #количество запрашиваемых анкет за один поиск

def get_user_data(user_id): 
    URL = 'https://api.vk.com/method/users.get'
    params = {
            'access_token': access_token,
        'v': '5.131', 'fields': 'domain, bdate, city, relation, sex'}

    res = requests.get(URL, params=params)
    response = res.json()
    
    username = response['response'][0]['first_name'] + ' ' + response['response'][0]['last_name'] 
    bdate = response['response'][0]['bdate']
    city = response['response'][0]['city']['id']
    relation = response['response'][0]['relation']
    clients_gender = response['response'][0]['sex']
    id = response['response'][0]['id']
    
    return bdate, city, relation, clients_gender, username
       

def search_users(gender_profile, relation_profile, city_profile):
    time.sleep(9)

    URL = 'https://api.vk.com/method/users.search'
    params = {
    
        'access_token': access_token,
        'sex': gender_profile,
        'city': city_profile,
#       'relation': relation_profile,
#        ''
        'count': NUM_READ_PROFILES,
        'v': '5.131', 
        'fields': 'id, bdate, city, relation, status, age_from, age_to, sex'}
    res = requests.get(URL, params=params)
    response = res.json()
    ids_of_users = response['response']['items']
    ids_profile_list = []
    print(response)

    for i in range(len(ids_of_users)):
        id_profile = ids_of_users[i]['id']
        ids_profile_list.append(id_profile)
    return ids_profile_list

  


 
# 
# if SELECT date_part('year', age(timestamp '2019-01-01'))

# class VK_Users_Search:
#     BASE_URL: str = 'https://api.vk.com/method/'
#     METHOD_USERS_SEARCH = 'users.search' 
#     PROTOCOL_VERSION = '5.131'
#     USER_IDS = 'randrange(10 ** 7)'

#     def __init__(self, user_id, access_token: str=None):
#         self.token=access_token
#         self.user_id=user_id

#     def _get_url(self, method_name: str) ->str:
#         return f'{self.BASE_URL}{method_name}'


def get_photos(id_profile):
    
    URL = 'https://api.vk.com/method/photos.getUserPhotos'
    params = {
        'access_token': access_token,
        'user_id': id_profile,
        
        'count': 10,
        'v': '5.131', 
        'extended': 1}

    res = requests.get(URL, params=params)
    response = res.json()
    photos = response['response']['items']
    photos_likes = []

    for i in range(len(photos)):
        likes = photos[i]['likes']['count'] + photos[i]['comments']['count']
        photos_likes.append([likes,i])

    photos_likes.sort(reverse=True)
    for i in range(min(3, len(photos))):
        print(photos[photos_likes[i][1]]['sizes'][1]['url'])

# get_photos(65465)

#     q = 'Vladislav%20Makarov' #Имя Фамилия
#     count = '10' #количество пользователей
#     birth_day = '07' #день рождения
#     birth_month = '08' #месяц рождения
#     birth_year = '1997' #год рождения
#     #сам запрос
#     response = urllib.request.urlopen(URL + 'users.search?q=' + q + '&count=' + count + '&birth_day=' + birth_day + '&birth_month=' + birth_month + '&birth_year=' + birth_year + '&v=5.52&access_token=' + token)
#     #преобразуем в json формат и в словарь
#     json_m = response.read().decode('utf-8')
#     data = json.loads(json_m)
#     ids = []
#     for i in data['response']['items']:
#         ids.append(i['id'])
#     return ids



# user = VK_Users_Search(token=access_token, user_id=user_id) 
# result = user.get_users()