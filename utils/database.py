import pymysql
from random import randint
import requests

def connect():
    try:
        return pymysql.connect(
            host='localhost',
            user='trade',
            port=3306,
            password='trade123',
            database='nft',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        return False

def create_tables():
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute('CREATE TABLE IF NOT EXISTS USERS (id int AUTO_INCREMENT, tg_id varchar(100), balance float, balance_drow float, is_worker int, is_verif int, can_withdraw int, ref bigint, username varchar(100), PRIMARY KEY (id))')
            cursor.execute('CREATE TABLE IF NOT EXISTS PROMOCODES (id int AUTO_INCREMENT, value float, is_used int, tg_id varchar(100), cod int, PRIMARY KEY (id))')
            cursor.execute('CREATE TABLE IF NOT EXISTS BUY_NFT (id int AUTO_INCREMENT, tg_id varchar(100), category varchar(100), paragraph varchar(100), PRIMARY KEY (id))')
            cursor.execute('CREATE TABLE IF NOT EXISTS FAVORITES (id int AUTO_INCREMENT, tg_id varchar(100), category varchar(100), paragraph varchar(100), PRIMARY KEY (id))')
        connection.commit()

def create_promo_db(tg_id, value):
    with connect() as connection:
        with connection.cursor() as cursor:
            rand = randint(1000000, 100000000)
            cursor.execute(f'SELECT * FROM PROMOCODES WHERE cod={rand}')
            if len(cursor.fetchall()) == 0:
                cursor.execute('INSERT INTO PROMOCODES (value, is_used, tg_id, cod) VALUES (%s, %s,  %s, %s)', (value, 0, tg_id, rand))
            else:
                return create_promo_db(tg_id, value)
        connection.commit()
        return rand

def get_promocodes(tg_id):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM PROMOCODES WHERE tg_id={tg_id}')
            return cursor.fetchall()

def get_workers():
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT tg_id FROM USERS WHERE is_worker=1')
            return cursor.fetchall()

def get_users():
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT tg_id FROM USERS')
            return cursor.fetchall()

def add_worker(tg_id):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE USERS SET is_worker=1 WHERE tg_id={tg_id}')
        connection.commit()

def add_mamont_db(tg_id, mamont_id):
    with connect() as connection:
        with connection.cursor() as cursor:
            mamont = get_user(mamont_id, '')
            if mamont['ref'] == 0:
                cursor.execute(f'UPDATE USERS SET ref={tg_id} WHERE tg_id={mamont_id}')
            else:
                return False
        connection.commit()
        return True

def del_mamont_db(mamont_id):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE USERS SET ref=0 WHERE tg_id={mamont_id}')
        connection.commit()
        return True

def get_mamonts(tg_id):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM USERS WHERE ref={tg_id}')
            return cursor.fetchall()

#USD = requests.get('https://cdn.cur.su/api/latest.json').json()['rates']['RUB']

USD = 61

def buy_nft_db(tg_id, category, paragraph, price):
    with connect() as connection:
        with connection.cursor() as cursor:
            if get_user(tg_id, '')['balance'] >= float(price.replace('$', '')) * USD:
                cursor.execute('UPDATE USERS SET balance=balance-%s WHERE tg_id=%s', (float(price.replace('$', '')) * USD, tg_id))
                cursor.execute('INSERT INTO BUY_NFT (tg_id, category, paragraph) VALUES (%s, %s, %s)', (tg_id, category, paragraph))
            else:
                return False
        connection.commit()
        return True

def set_mamont_verif(mamont_id, value):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE USERS SET is_verif={value} WHERE tg_id={mamont_id}')
        connection.commit()

def set_mamont_vivod(mamont_id, value):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE USERS SET can_withdraw={value} WHERE tg_id={mamont_id}')
        connection.commit()

def set_mamont_balance_db(mamont_id, value):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE USERS SET balance={value} WHERE tg_id={mamont_id}')
        connection.commit()

def set_nft_price(tg_id, category, paragraph, price):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE BUY_NFT SET price={price} WHERE category="{category}" AND paragraph="{paragraph}" AND tg_id={tg_id}')
        connection.commit()

def get_nft_price(tg_id, category, paragraph):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT price FROM BUY_NFT WHERE category="{category}" AND paragraph="{paragraph}" AND tg_id={tg_id}')
            return cursor.fetchone()

def get_nft_sell_worker(tg_id, category, paragraph):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM BUY_NFT WHERE category="{category}" AND paragraph="{paragraph}" AND tg_id={tg_id}')
            return cursor.fetchone()

def nft_sell_worker(tg_id, category, paragraph, price):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM BUY_NFT WHERE category="{category}" AND paragraph="{paragraph}" AND tg_id={tg_id}')
        connection.commit()
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE USERS SET balance=balance+{price*USD} WHERE tg_id={tg_id}')
        connection.commit()

def like_nft_db(tg_id, category, paragraph):
    with connect() as connection:
        with connection.cursor() as cursor:
            if get_like(tg_id, category, paragraph):
                cursor.execute(f'DELETE FROM FAVORITES WHERE category="{category}" AND paragraph="{paragraph}" AND tg_id={tg_id}')
            else:
                cursor.execute('INSERT INTO FAVORITES (tg_id, category, paragraph) VALUES (%s, %s, %s)', (tg_id, category, paragraph))
        connection.commit()

def get_like(tg_id, category, paragraph):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM FAVORITES WHERE category="{category}" AND paragraph="{paragraph}" AND tg_id={tg_id}')
            like = cursor.fetchone()
            if like == None:
                return False
            if len(like) == 0:
                return False
            return True
def get_likes(category, paragraph):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM FAVORITES WHERE category="{category}" AND paragraph="{paragraph}"')
            return cursor.fetchall()

def get_likes_user(tg_id):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM FAVORITES WHERE tg_id={tg_id}')
            return cursor.fetchall()

def get_buy_nft(tg_id):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM BUY_NFT WHERE tg_id={tg_id}')
            return cursor.fetchall()

def create_users(tg_id, username, ref=0):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO `USERS` (`tg_id`, `balance`, `balance_drow`, `is_worker`, `is_verif`, `can_withdraw`, `ref`, `username`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (tg_id, 0, 0, 0, 0, 1, ref, username))
        connection.commit()

def get_user(tg_id, username, ref=0):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM USERS WHERE tg_id={tg_id}')
            user = cursor.fetchone()
            if user == None:
                create_users(tg_id, username, ref)
                return get_user(tg_id, username, ref)
            return user

def show_users():
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM USERS')
            print(cursor.fetchall())

