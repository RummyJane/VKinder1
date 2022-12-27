import psycopg2
from config import password


def clear_db():
    with conn.cursor() as cur:
        cur.execute('''delete from bot_clients where 1=1;''')
    conn.commit


def close_db():
    conn.close()


# def create_db(conn):
#     with conn.cursor() as cur:
#         cur.execute(
#         '''CREATE TABLE IF NOT EXISTS bot_clients(
#         id INTEGER NOT NULL,
#         id_profile INTEGER NOT NULL, 
#         profile_status VARCHAR(10) DEFAULT 'new',
#         CONSTRAINT comb_id PRIMARY KEY (id, id_profile));'''
#         )


def get_next_profile(user_id):
    with conn.cursor() as cur:
        cur.execute(
        '''select id_profile 
        from bot_clients 
        where id = %s and profile_status = 'new'
        limit 1;''', ((user_id,)))
    
        profile_id = int(cur.fetchone()[0])
        return profile_id


def mark_as_shown(user_id, candidate_id):
    with conn.cursor() as cur:
        cur.execute(
        '''update bot_clients 
        set profile_status = 'seen'
        where id = %s and id_profile = %s;''', (user_id, candidate_id))
    conn.commit


def add_client(user_id, ids_profile_list, profile_status):
    with conn.cursor() as cur:
        for id_profile in ids_profile_list:
            if id_profile is not None:
                cur.execute(
                '''INSERT INTO bot_clients(id, id_profile, profile_status) 
                    VALUES(%s, %s, %s);''', (user_id, id_profile, profile_status))
                    # VALUES(%s, %s, %s) RETURNING id, id_profile, profile_status;''', (user_id, id_profile, profile_status))
        conn.commit()


conn = psycopg2.connect(database="vk_users_get", user="postgres", password=password)
clear_db()


    
