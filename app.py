# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, redirect, request, url_for, \
    session, send_from_directory, current_app, send_file
from src import query_processor
import sqlite3 as sql
import os
from config import Config
from model import model_service 
import sys
import glob


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
        return redirect(url_for('.search_request', search_text=search_text))
    return render_template('search.html', title="Search")


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():  # when we searching again from results page

    # res = session.get('data', None)
    search_text = request.form.get('search_text')
    search_text_old = request.args['search_text']
    res = query_processor.get_search_result(search_text_old, False)
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
    article_path = 'articles/' + str(article_id)+'*'
    jpgFilenamesList = glob.glob(article_path)
    if len(jpgFilenamesList) > 0:
        uploads = os.path.join(current_app.root_path, jpgFilenamesList[0])
        return send_file(uploads)
    return 'not found'


@app.errorhandler(400)
def br(e):
    return render_template('404.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/hall_of_fame')
def hall_of_fame():
    return render_template('Hall_of_fame.html')


if __name__ == '__main__':
    model_service.retrain_model()
    model = model_service.Model()
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
