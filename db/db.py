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
  text TEXT NOT NULL
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
articles = [(1, 'Первая запись', 'Первое описание'),
            (2, 'Вторая запись', 'Второе описание'),
            (3, 'Третья запись', 'Третье описание'),
            (4, 'Четвертая запись', 'Четвертое описание')]

datasets = [(1, 1, 'dataset_1'),
            (2, 1, 'dataset_2'),
            (3, 3, 'dataset_3'),
            (4, 4, 'dataset_4'),
            (5, 5, 'dataset_5')]

cursor.executemany('''
INSERT INTO articles (id, title, text)
VALUES (?,?,?)''', articles)

cursor.executemany('''
INSERT INTO datasets (id, article_id, title)
VALUES (?,?,?)''', datasets)

conn.commit()
conn.close()
