import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE articles
                  (title, text)
               """)



# Вставляем множество данных
articles = [('Первая запись', 'Первое описание'),
            ('Вторая запись', 'Второе описание'),
            ('Третья запись', 'Третье описание'),
            ('Четвертая запись', 'Четвертое описание')]

cursor.executemany("INSERT INTO articles VALUES (?,?)", articles)
conn.commit()
conn.close()
