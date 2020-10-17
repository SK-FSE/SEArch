import sqlite3


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('articles.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn


def get_search_result(query):
    conn = db_connection()
    cursor = conn.cursor()
    cursor = conn.execute('SELECT * FROM articles')
    articles = [
        dict(id=row[0], author=row[1], language=row[2], title=row[3])
        for row in cursor.fetchall()
    ]
    conn.close()
    return ['dear',
            ' ',
            query,
            ' ',
            'found author',
            ' ',
            articles[0]['author']]
