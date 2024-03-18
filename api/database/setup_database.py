
import sqlite3
import pathlib

DB_DIR = pathlib.Path(__file__).parent

TABLES = [
    '''
    CREATE TABLE IF NOT EXISTS Links (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL,
        time INTEGER NOT NULL
    )
    '''
]


def setup_database(app):
    print(f'config: {app.config}')
    db_name = app.config['database']['prod_name']
    if app.config['test']:
        db_name = app.config['database']['test_name']
    db = sqlite3.connect(f'{DB_DIR}/{db_name}.db')
    initial_tables(db)
    app.db = db

def initial_tables(db):
    cursor = db.cursor()
    for table in TABLES:
        cursor.execute(table)
    db.commit()
