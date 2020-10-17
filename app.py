# -*- coding: utf-8 -*-

from flask import Flask, render_template
from src import query_processor


app = Flask(__name__)


@app.route('/search/<query>')
def search(query=None):
    result = ''.join(query_processor.get_search_result(query))
    return render_template('hello.html', query=result)


@app.route('/')
def root(query=None):
    return 'go to /search/smth'


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
