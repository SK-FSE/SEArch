import sqlite3 as sql
"""
input_examples: input = [('sth_1', 'id_1'), 
                         ('sth_2', 'id_2'), 
                         ('sth_3', 'id_3')] 
              or input = ('sth_1', 'id_1')
ids_example: ids = [(id_1,),(id_3,),(id_4,)] 
          or ids = [(id_1,)]
 """
def set_dataset_by_id(input):
    try:
            with sql.connect("mydatabase.db") as con:
                cur = con.cursor()

                if type(input) is list:
                    cur.executemany('''UPDATE datasets SET dataset = ? 
                                        WHERE article_id=?''', input)
                    con.commit()
                    msg = "dataset successfully set"
                else:
                    cur.execute('''UPDATE datasets SET dataset = ? 
                                    WHERE article_id=?''', input)
                    con.commit()
                    msg = "dataset successfully set"
    except Set_Dataset_Error:
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
                    msg = "article description successfully set"
                else:
                    cur.execute('''UPDATE articles SET text = ? 
                                    WHERE id=?''', input)
                    con.commit()
                    msg = "article description successfully set"        
    except Set_Article_Description_Error:
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
                    msg = "article successfully set"
                else:
                    cur.execute('''UPDATE articles SET title =? 
                                    WHERE id=?''', input)
                    con.commit()
                    msg = "article successfully set"
    except Set_Article_Error:
        con.rollback()
        msg = "error in set_article_by_id"
        print(msg)

# =============================================================================


def get_article_description_by_id(ids):
    try:
            with sql.connect("mydatabase.db") as con:
                cur = con.cursor()

                for id in ids:
                    cur.execute('''SELECT text FROM articles 
                                    WHERE id=?''', id)
                    result = cur.fetchall()
    except Get_Article_Description_Error:
        msg = "article_description/s not found"
        print(msg)

def get_article_by_id(ids):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()
            
            for id in ids:
                cur.execute('''SELECT title FROM articles 
                                WHERE id=?''', id)
                result = cur.fetchall()
    except Get_Article_Error:
        msg = "article/s not found"
        print(msg)

def get_dataset_by_id(ids):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()

            for id in ids:
                cur.execute('''SELECT dataset FROM datasets 
                                WHERE article_id=?''', id)
                result = cur.fetchall()
    except Get_Dataset_Error:
        msg = "dataset/s not found"
        print(msg)