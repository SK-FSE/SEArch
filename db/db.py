import sqlite3
 
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
 
# Создание таблицы
cursor.execute("""CREATE TABLE albums
                  (title, text)
               """)



# Вставляем множество данных в таблицу используя безопасный метод "?"
albums = [('Первая запись', 'Первое описание'),
          ('Вторая запись', 'Второе описание'),
          ('Третья запись', 'Третье описание'),
          ('Четвертая запись', 'Четвертое описание')]
 
cursor.executemany("INSERT INTO albums VALUES (?,?)", albums)
conn.commit()
conn.close()