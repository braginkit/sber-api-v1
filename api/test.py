
import sqlite3

from sys import maxsize as maxint
from main import setup_app
from http import HTTPStatus
from urllib.parse import urlparse

DB_NAME = 'browser_history_test'
DEFAULT_TIME = 10


async def is_valid_json(resp_json, expected_resp_json):
    resp_json_key_count = 0
    for key in resp_json:
        resp_json_key_count += 1
        if key not in expected_resp_json:
            is_invalid_error = f'{key} not in {expected_resp_json}'
            print(is_invalid_error)
            return False
        if not isinstance(resp_json[key], type(expected_resp_json[key])):
            is_invalid_error = f'type(resp_json[key]) != ' \
                               f'expected_resp_json[key] ' \
                               f'{type(resp_json[key])} != ' \
                               f'{expected_resp_json[key]} ' \
                               f'(key={key})'
            print(is_invalid_error)
            return False
        if resp_json[key] != expected_resp_json[key]:
            is_invalid_error = f'resp_json[key] !=  ' \
                               f'expected_resp_json[key] ' \
                               f'{resp_json[key]} != ' \
                               f'{expected_resp_json[key]} ' \
                               f'(key={key})'
            print(is_invalid_error)
            return False
    if len(expected_resp_json) != resp_json_key_count:
        is_invalid_error = f'len(expected_resp_json) !=  ' \
                           f'resp_json_key_count ' \
                           f'{len(expected_resp_json)} != ' \
                           f'{resp_json_key_count}'
        print(is_invalid_error)
        return False

    return True


def initial_test(
    delete_data=True,  # удаление всех записей
    queries_to_insert=[],
    conn=None,
    ):
    if conn is None:
        db = sqlite3.connect(f'database/{DB_NAME}.db')
        cursor = db.cursor()
    if delete_data:
        delete_data_from_db(cursor)
    if queries_to_insert:
        insert_data(cursor, queries_to_insert)
    db.commit()
    return conn


def delete_data_from_db(cursor):
    delete_quries = [
        f'DELETE FROM Links',
    ]
    for query in delete_quries:
        cursor.execute(query)


def insert_data(cursor, queries_to_insert):
    for query in queries_to_insert:
        cursor.execute(query)

async def test_get_visited_domains_empty(aiohttp_client):
    expected_json = {
        'domains': [],
        'status': 'ok'
    }
    client = await aiohttp_client(setup_app)
    initial_test()
    params = [
        ('from', 0),
        ('to', maxint),
    ]
    resp = await client.get(
        '/visited_domains/',
        params=params,
    )
    status = resp.status
    assert status == HTTPStatus.OK
    resp_json = await resp.json()
    assert await is_valid_json(resp_json, expected_json)


async def test_get_visited_domains_no_duplicate(aiohttp_client):
    links = [
        'https://ya.ru/',
        'https://ya.com/'
    ]
    expected_json = {
        'domains': list(set([urlparse(link).netloc for link in links])),
        'status': 'ok'
    }
    queries_to_insert = [
        f'INSERT INTO Links (url, time) VALUES '
        f'("{link}", {DEFAULT_TIME})' for link in links
    ]
    client = await aiohttp_client(setup_app)
    initial_test(queries_to_insert=queries_to_insert)
    params = [
        ('from', 0),
        ('to', maxint),
    ]
    resp = await client.get(
        '/visited_domains/',
        params=params,
    )
    status = resp.status
    assert status == HTTPStatus.OK
    resp_json = await resp.json()
    assert await is_valid_json(resp_json, expected_json)


async def test_get_visited_domains_with_duplicate(aiohttp_client):
    links = [
        'https://ya.ru/',
        'https://ya.com/',
        'https://ya.ru/',
        'https://ya.com/'
    ]
    expected_json = {
        'domains': list(set([urlparse(link).netloc for link in links])),
        'status': 'ok'
    }
    queries_to_insert = [
        f'INSERT INTO Links (url, time) VALUES '
        f'("{link}", {DEFAULT_TIME})' for link in links
    ]
    client = await aiohttp_client(setup_app)
    initial_test(queries_to_insert=queries_to_insert)
    params = [
        ('from', 0),
        ('to', maxint),
    ]
    resp = await client.get(
        '/visited_domains/',
        params=params,
    )
    status = resp.status
    assert status == HTTPStatus.OK
    resp_json = await resp.json()
    assert await is_valid_json(resp_json, expected_json)


async def test_get_visited_domains_empty_time(aiohttp_client):
    links = [
        'https://ya.ru/',
        'https://ya.com/',
        'https://ya.ru/',
        'https://ya.com/'
    ]
    expected_json = {
        'domains': [],
        'status': 'ok'
    }
    queries_to_insert = [
        f'INSERT INTO Links (url, time) VALUES '
        f'("{link}", {DEFAULT_TIME})' for link in links
    ]
    client = await aiohttp_client(setup_app)
    initial_test(queries_to_insert=queries_to_insert)
    params = [
        ('from', 20),
        ('to', maxint),
    ]
    resp = await client.get(
        '/visited_domains/',
        params=params,
    )
    status = resp.status
    assert status == HTTPStatus.OK
    resp_json = await resp.json()
    assert await is_valid_json(resp_json, expected_json)


async def test_get_visited_domains_limited_by_time(aiohttp_client):
    links = [
        'https://ya.ru/',
        'https://ya.com/',
    ]
    links2 = [
        'https://google.ru/',
        'https://google.com/',
    ]
    expected_json = {
        'domains': list(set([urlparse(link).netloc for link in links])),
        'status': 'ok'
    }
    queries_to_insert = [
        f'INSERT INTO Links (url, time) VALUES '
        f'("{link}", {DEFAULT_TIME})' for link in links
    ]
    queries_to_insert += [
        f'INSERT INTO Links (url, time) VALUES '
        f'("{link}", {DEFAULT_TIME + 10})' for link in links2
    ]
    client = await aiohttp_client(setup_app)
    initial_test(queries_to_insert=queries_to_insert)
    params = [
        ('from', 0),
        ('to', DEFAULT_TIME + 1),
    ]
    resp = await client.get(
        '/visited_domains/',
        params=params,
    )
    status = resp.status
    assert status == HTTPStatus.OK
    resp_json = await resp.json()
    assert await is_valid_json(resp_json, expected_json)


async def test_post_visited_links(aiohttp_client):
    links = [
        'https://ya.ru/',
        'https://ya.com/',
    ]
    expected_json = {'status': 'ok'}
    client = await aiohttp_client(setup_app)
    initial_test()
    resp = await client.post(
        '/visited_links/',
        json={'links': links},
    )
    status = resp.status
    assert status == HTTPStatus.OK
    resp_json = await resp.json()
    assert await is_valid_json(resp_json, expected_json)


async def test_post_visited_links_empty(aiohttp_client):
    links = []
    expected_json = {'status': 'ok'}
    client = await aiohttp_client(setup_app)
    initial_test()
    resp = await client.post(
        '/visited_links/',
        json={'links': links},
    )
    status = resp.status
    assert status == HTTPStatus.OK
    resp_json = await resp.json()
    assert await is_valid_json(resp_json, expected_json)


async def test_post_visited_links_key_error(aiohttp_client):
    links = []
    client = await aiohttp_client(setup_app)
    initial_test()
    resp = await client.post(
        '/visited_links/',
        json={'bad_key': links},
    )
    status = resp.status
    assert status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_post_visited_links_urls_error(aiohttp_client):
    links = [1, 2, 3]
    client = await aiohttp_client(setup_app)
    initial_test()
    resp = await client.post(
        '/visited_links/',
        json={'links': links},
    )
    status = resp.status
    assert status == HTTPStatus.UNPROCESSABLE_ENTITY
