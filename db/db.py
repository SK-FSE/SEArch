import sqlite3
from os import path, listdir, mkdir
import os, os.path

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS articles')
cursor.execute('DROP TABLE IF EXISTS datasets')

# Создание таблицы
cursor.execute('''
CREATE TABLE articles (
  id INTEGER PRIMARY KEY,
  path TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE datasets (
  id INTEGER PRIMARY KEY,
  article_id INTEGER,
  title TEXT NOT NULL
)
''')

# Вставляем множество данных
articles=[]
for filename in listdir('../articles/'):
    articles.append(tuple([int(filename.split('-')[0]), '/articles/'+filename ]))

datasets = [(1, 1, 'dataset_1'),
            (2, 1, 'dataset_2'),
            (3, 3, 'dataset_3'),
            (4, 4, 'dataset_4'),
            (5, 5, 'dataset_5')]

cursor.executemany('''
INSERT INTO articles (id, path)
VALUES (?,?)''', articles)

cursor.executemany('''
INSERT INTO datasets (id, article_id, title)
VALUES (?,?,?)''', datasets)

conn.commit()
conn.close()
