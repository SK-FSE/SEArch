import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE articles')

# Создание таблицы
cursor.execute('''
CREATE TABLE articles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  text TEXT NOT NULL
)
''')

# Вставляем множество данных
articles = [('Первая запись', 'Первое описание'),
            ('Вторая запись', 'Второе описание'),
            ('Третья запись', 'Третье описание'),
            ('Четвертая запись', 'Четвертое описание')]

cursor.executemany('''
INSERT INTO articles (title, text)
VALUES (?,?)''', articles)

conn.commit()
conn.close()
