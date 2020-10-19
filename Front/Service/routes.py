# -*- coding: utf-8 -*-
import os
from Service import app
from flask import render_template, flash, redirect, request, url_for, \
    session, send_from_directory, current_app, send_file

import os



def res_giver(query):
    res = {'query': query,
               'is_filter': 0,
               'total': 3,
               'hits': [
                   {'title': 'Title1', 'year': '1998', 'id': 1, 'abstract': 'text1',
                    'article_piece': 'Hello world, You\'re rock sucker.', 'author': 'author12'},
                   {'title': 'Title2', 'year': '2005', 'id': 2, 'abstract': 'text1', 'article_piece': 'Hello world, You\'re sock sucker.', 'author': 'author2'},
                   {'title': 'Title3', 'year': '2005', 'id': 3, 'abstract': 'text1', 'article_piece': 'Hello world, You\'re wok sucker.', 'author': 'author3'}]}
    return res


def redirect_to_article(id_a, data):
    return redirect(url_for('/search/results/'+ str(id_a), data=data))


@app.route('/')
def route():
    return redirect('/search')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_text = request.form.get('search_text')
        session['data'] = res_giver(search_text)
        return redirect('/search/results')
    return render_template('search.html', title="Search")


@app.route('/search/results', methods=['GET', 'POST'])
def search_request(): #when we searching again from results page

    res = session.get('data', None)
    search_text = request.form.get('search_text')
    if search_text != res['query'] and search_text is not None and search_text != '':
        res = res_giver(search_text)
        session['data'] = res
    return render_template('results.html', res=res)


# @app.route('/search/results/<int:article_id>', methods=['GET'])
# def show_article_info(article_id):
#     data = session.get('data', None)
#     article = [x for x in data['hits'] if x['id'] == article_id][0]
#     return render_template('article_info.html', title="Article info", article=article)


@app.route('/search/results/<int:article_id>', methods=['GET'])
def download(article_id):
    data = session.get('data', None)
    uploads = os.path.join(current_app.root_path, 'Files', str(article_id)+'.pdf')
    return send_file(uploads)
