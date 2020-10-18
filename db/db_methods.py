import sqlite3 as sql


def set_dataset_by_id(article_id, dataset):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()
            cur.execute('''UPDATE datasets SET title = ?
                            WHERE article_id=?''', (dataset, article_id))
            con.commit()
    except Exception as e:
        con.rollback()
        msg = "error in set_dataset_by_id"
        print(msg)


def set_article_description_by_id(id, article_description):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()
            cur.execute('''UPDATE articles SET title = ?
                            WHERE id=?''', (article_description, id))
            con.commit()
    except Exception as e:
        con.rollback()
        msg = "set_article_description_by_id"
        print(msg)


def set_article_by_id(id, article):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()
            cur.execute('''UPDATE articles SET text =?
                            WHERE id=?''', (article, id))
            con.commit()
    except Exception as e:
        con.rollback()
        msg = "error in set_article_by_id"
        print(msg)

# =============================================================================


def get_article_descriptions_by_ids(ids):
    try:
        with sql.connect("mydatabase.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            result = []
            for id in ids:
                cur.execute('''SELECT title FROM articles
                                WHERE id=?''',  [id])
                rows = cur.fetchall()
                result.append(rows[0]['text'])
            return result
    except Exception as e:
        msg = "article_description/s not found"
        print(msg)


def get_articles_by_ids(ids):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()
            result = []
            for id in ids:
                cur.execute('''SELECT * FROM articles
                                WHERE id=?''',  [id])
                rows = cur.fetchone()
                result.append(rows)
            return result
    except Exception as e:
        msg = "article/s not found"
        print(msg)


def get_datasets_by_ids(ids):
    try:
        with sql.connect("mydatabase.db") as con:
            cur = con.cursor()
            result = []
            for id in ids:
                cur.execute('''SELECT * FROM datasets
                                WHERE article_id=?''', [id])
                rows = cur.fetchone()
                result.append(rows)
            return result
    except Exception as e:
        msg = "dataset/s not found"
        print(msg)
