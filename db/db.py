import sqlite3

conn = sqlite3.connect('articles.sqlite')

cursor = conn.cursor()
create_table_query = '''
CREATE TABLE articles (
    id integer PRIMARY KEY,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
)'''
insert_dummy_articles_query = '''
INSERT INTO articles (author, language, title) VALUES (?, ?, ?)
'''
drop_articles_query = ''' DROP TABLE articles'''

cursor.execute(drop_articles_query)
cursor.execute(create_table_query)
cursor.execute(insert_dummy_articles_query, ['lala', 'lolo', 'lili'])
conn.commit()
conn.close()
