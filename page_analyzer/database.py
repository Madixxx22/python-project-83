import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def get_urls() -> list:
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute('SELECT id, name FROM urls ORDER BY id DESC;')
        data = cur.fetchall()
    conn.close()
    return data


def get_url_by_name(name: str) -> dict:
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT id, name, created_at
                   FROM urls
                   WHERE name = (%s)
        '''
        cur.execute(query, [name])
        data = cur.fetchone()
    conn.close()
    return data


def get_url_by_id(id: int) -> dict:
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT id, name, created_at
                   FROM urls
                   WHERE id = (%s)
                '''
        cur.execute(query, [id])
        data = cur.fetchone()
    conn.close()
    return data


def get_id_url_by_name(name: str) -> dict:
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT id
                   FROM urls
                   WHERE name = (%s)
        '''
        cur.execute(query, [name])
        data = cur.fetchone()
    conn.close()
    return data


def get_url_checks(url_id: int) -> list:
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT id, url_id, status_code, h1, title,
                          description, created_at
                   FROM url_checks
                   WHERE url_id = (%s)
                   ORDER BY id DESC;
                '''
        cur.execute(query, [url_id])
        data = cur.fetchall()
    conn.close()
    return data


def get_url_check_last(url_id: int) -> list:
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT status_code, created_at
                   FROM url_checks
                   WHERE url_id = (%s)
                   ORDER BY id DESC;
                '''
        cur.execute(query, [url_id])
        data = cur.fetchone()
    conn.close()
    return data


def create_url(data: dict):
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''INSERT INTO urls (name, created_at)
                   VALUES (%s, %s);
                '''
        cur.execute(query, (data['url'], data['created_at']))
        conn.commit()
    conn.close()


def create_check(data: dict):
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''INSERT INTO url_checks (url_id, created_at)
                   VALUES (%s, %s);
                '''
        cur.execute(query, (data['url_id'], data['created_at']))
        conn.commit()
    conn.close()
