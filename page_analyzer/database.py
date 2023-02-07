import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def get_urls():
    data = None
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute('SELECT id, name FROM urls ORDER BY id DESC;')
        data = cur.fetchall()
    conn.close()
    return data


def create_url(data):
    conn = get_connection()
    with conn.cursor() as cur:
        query = '''INSERT INTO urls (name, created_at)
                   VALUES (%s, %s);'''
        cur.execute(query, (data['url'], data['date']))
        conn.commit()
    conn.close()


def get_id_url_by_name(name):
    data = None
    conn = get_connection()
    with conn.cursor() as cur:
        query = '''SELECT id
                   FROM urls
                   WHERE name = (%s)
        '''
        cur.execute(query, [name])
        data = cur.fetchone()
    conn.close()
    return data


def get_url_by_name(name):
    data = None
    conn = get_connection()
    with conn.cursor() as cur:
        query = '''SELECT *
                   FROM urls
                   WHERE name = (%s)
        '''
        cur.execute(query, [name])
        data = cur.fetchone()
    conn.close()
    return data


def get_url_by_id(id):
    data = None
    conn = get_connection()
    with conn.cursor() as cur:
        query = '''SELECT *
                   FROM urls
                   WHERE id = (%s)
                '''
        cur.execute(query, [id])
        data = cur.fetchone()
    conn.close()
    return data
