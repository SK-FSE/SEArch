"""
input_examples: input = [('sth_1', 'id_1'),
                         ('sth_2', 'id_2'),
                         ('sth_3', 'id_3')]
              or input = ('sth_1', 'id_1')
 """
import sqlite3 as sql


def set_dataset_by_id(input):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()
            if type(input) is list:
                cur.executemany('''UPDATE datasets SET dataset = ?
                                    WHERE article_id=?''', input)
                con.commit()
            else:
                cur.execute('''UPDATE datasets SET dataset = ?
                                WHERE article_id=?''', input)
                con.commit()
    except Exception as e:
        con.rollback()
        msg = "error in set_dataset_by_id"
        print(msg)


def set_article_description_by_id(input):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()
            if type(input) is list:
                cur.executemany('''UPDATE articles SET text = ?
                                    WHERE id=?''', input)
                con.commit()
            else:
                cur.execute('''UPDATE articles SET text = ?
                                WHERE id=?''', input)
                con.commit()      
    except Exception as e:
        con.rollback()
        msg = "set_article_description_by_id"
        print(msg)


def set_article_by_id(input):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()
            if type(input) is list:
                cur.executemany('''UPDATE articles SET title = ?
                                    WHERE id=?''', input)
                con.commit()
            else:
                cur.execute('''UPDATE articles SET title =?
                                WHERE id=?''', input)
                con.commit()
    except Exception as e:
        con.rollback()
        msg = "error in set_article_by_id"
        print(msg)

# =============================================================================


def get_article_description_by_id(ids):
    try:
        with sql.connect("mydatabase.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            result = []

            for id in ids:
                cur.execute('''SELECT text FROM articles
                                WHERE id=?''', id)
                rows = cur.fetchall()
                result.append(rows[0]['text'])
            return result
    except Exception as e:
        msg = "article_description/s not found"
        print(msg)


def get_article_by_id(ids):
    try:
        with sql.connect("mydatabase.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            result = []
            
            for id in ids:
                cur.execute('''SELECT title FROM articles
                                WHERE id=?''', id)
                rows = cur.fetchall()
                result.append(rows[0]['title'])
            return result
    except Exception as e:
        msg = "article/s not found"
        print(msg)


def get_dataset_by_id(ids):
    try:
        with sql.connect("mydatabase.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            result = []
            for id in ids:
                cur.execute('''SELECT dataset FROM datasets
                                WHERE article_id=?''', [id])
                rows = cur.fetchall()
                result.append(rows[0]['dataset'])
            return result
    except Exception as e:
        msg = "dataset/s not found"
        print(msg)
