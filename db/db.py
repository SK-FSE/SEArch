import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS articles')
cursor.execute('DROP TABLE IF EXISTS datasets')

# Создание таблицы
cursor.execute('''
CREATE TABLE articles (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  text TEXT NOT NULL,
  article_date TEXT NOT_NULL
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
articles = [(1, 'Первая запись', 'Первое описание', '2020-06-12'),
            (2, 'Вторая запись', 'Второе описание', '2020-07-12'),
            (3, 'Третья запись', 'Третье описание', '2020-08-12'),
            (4, 'Четвертая запись', 'Четвертое описание', '2020-09-12')]

datasets = [(1, 1, 'dataset_1'),
            (2, 1, 'dataset_2'),
            (3, 3, 'dataset_3'),
            (4, 4, 'dataset_4'),
            (5, 5, 'dataset_5')]

cursor.executemany('''
INSERT INTO articles (id, title, text, article_date)
VALUES (?,?,?,?)''', articles)

cursor.executemany('''
INSERT INTO datasets (id, article_id, title)
VALUES (?,?,?)''', datasets)

conn.commit()
conn.close()