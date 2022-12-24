import vk_api
import requests
# from config import access_token
from random import randrange
import psycopg2
from config import password
from time import strptime


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS bot_clients(
            id SERIAL PRIMARY KEY UNIQUE,
            id_profile INTEGER NOT NULL, 
            profile_status VARCHAR(10));''')


def add_client(conn, user_id, ids_profile_list):
    with conn.cursor() as cur:
        if user_id != id and ids_profile_list is not None:
            for id_profile in ids_profile_list:
                if id_profile is not None:
                    cur.execute(
                    '''INSERT INTO bot_clients(id, id_profile, profile_status) 
                        VALUES (%s, %s, %s) RETURNING id, id_profile, profile_status);'''), (user_id, ids_profile_list, 'new')
                    user_id = cur.fetchone()[0]
                    print(user_id)


with psycopg2.connect(database="vk_users_get", user="postgres", password=password) as conn:

    create_db(conn)
    phonelist1 = ['234234234', '6789403', '90543']
    phonelist2 = ['6555554', '+7897778803', '+122223390543']
    # add_client(conn, 'Ivan', 'Sanin', 's.ivan@yandex.com', phonelist1)
    
    
