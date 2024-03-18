
async def add_new_urls(db, urls, time):
    cursor = db.cursor()
    for url in urls:
        cursor.execute(
            'INSERT INTO Links (url, time) VALUES (?, ?)',
            (url, time),
        )
    db.commit()

async def get_urls(db, start_time, end_time):
    cursor = db.cursor()
    cursor.row_factory = lambda cursor, row: row[0]
    query = f'''
        SELECT url from Links
        where {start_time} <= time and time <= {end_time}
    '''
    cursor.execute(query)
    res = cursor.fetchall()
    return res
