from config import access_token
import requests
import time
import pandas as pd
import vk_api

vk = vk_api.VkApi(token='access_token')

data = pd.read_csv('in.txt', encoding = 'cp1251')
t={} #создаем словарь для хранения данных, получаемых от API VK
for j in range(0, len(data)): #запускаем поиск по массиву
    #Далее следует обращение к API с нашими параметрами:
    t[j]=vk.users.search(q = data['N'][j] + ' ' + data['F'][j], birth_day = data['D'][j], \ birth_month = data['M'][j], birth_year = data['Y'][j], count = 1000, fields='bdate, city')
    for h in (t[j]['items']): #Сохраняем результаты поиска в файл"users.txt"
        with open('users.txt','a') as f1:
            f1.write((str(data['id'][j]) + ';' #ID исходный
              + str(t[j]['count']) + ';' #Количество найденных пользователей
              + str(h['id']) + ';' #ID пользователя VK
              + h['last_name'] + ';' #Фамилия
              + h['first_name'] + ';' #Имя
              + h.get('bdate','') + ';' #Дата рождения
              + h.get('city',{}).get('title','') #У города несколько параметров - нам нужно название: title
              + ';\n').encode('cp1251', 'replace').decode('cp1251'))#Для удаления нестандартных символов, которые могут вызывать ошибки

#  token = input("Token: ")

# class DisplayTypes(BaseModel):
#     page: str = "page"
#     popup: str = "popup"


# class VKSearchUsers(BaseModel):
#     user_ids: str = "friends"
#     WALL: str = "wall"

#     def scope_list(self):
#         return [self.FRIENDS, self.WALL]

#     @property
    # def scope(self):
    #     return ','.join(self.scope_list())


APP_ID = 51498475


# class VK_Users_Search():
URL = 'https://api.vk.com/method/users.get'
params = {
    'q': '3344',
     'access_token': app_token,
      'v': '5.131', 'fields': 'sex, city, bdate, relation, domain ' }


    # def __init__(self, token, version) -> None:
    #     self.params = {'access.token': token, 'version': version}

res = requests.get(URL, params=params)
res = res['response']['items']
print(res.json())


#  if sex={%s}

'''получить расширенную инф. по группе с пом. метода groups.getById'''
# target_group_id = ','.join([str[group_id]) for group in target_groups])
# pprint(target_group_id) или group['name']



'''photo_sizes: checkbox

1 — возвращать доступные размеры фотографии в специальном формате. По умолчанию: 0. '''
