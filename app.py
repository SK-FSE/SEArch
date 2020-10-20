# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, redirect, request, url_for, \
    session, send_from_directory, current_app, send_file
from src import query_processor
import sqlite3 as sql
import os
from config import Config
from model import model_service 

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def route():
    return redirect('/search')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_text = request.form.get('search_text')
        session['data'] = query_processor.get_search_result(search_text, False)
        return redirect('/search/results')
    return render_template('search.html', title="Search")

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():  # when we searching again from results page

    res = session.get('data', None)
    search_text = request.form.get('search_text')
    if search_text != res['query'] and search_text is not None and search_text != '':
        if request.form['button'] == 'Basic':
            is_deep = False
        elif request.form['button'] == 'Deep':
            is_deep = True
        res = query_processor.get_search_result(search_text, is_deep)
        session['data'] = res
    return render_template('results.html', res=res)


@app.route('/search/results/<int:article_id>', methods=['GET'])
def download(article_id):
    data = session.get('data', None)
    uploads = os.path.join(current_app.root_path, 'Files', str(article_id)+'.pdf')
    return send_file(uploads)


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
    print('preparing model')
    model = model_service.Model()
    print('model ready')
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
