# -*- coding: utf-8 -*-

from flask import Flask, render_template
from src import query_processor
import sqlite3 as sql

app = Flask(__name__)


# frontend simulation. Frontend sends query to get_search_result
# get_search_result is an entrypoint for backend
@app.route('/search/<query>')
def search(query=None):
    result = ''.join(query_processor.get_search_result(query))
    return render_template('hello.html', query=result)


@app.route('/')
def root(query=None):
    return 'go to /search/smth'


# tmp router to show that db works correctly
@app.route('/list')
def list():
    con = sql.connect('mydatabase.db')
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute('select * from articles')
    rows = cur.fetchall()

    cur.execute('select * from datasets')
    datasets = cur.fetchall()

    con.close()
    return render_template('list.html', rows=rows, datasets=datasets)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
