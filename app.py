# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from src import query_processor
import sqlite3 as sql

app = Flask(__name__)


@app.route("/search/<query>")
def search(query=None):
    result = ''.join(query_processor.get_search_result(query))
    return render_template('hello.html', query=result)


@app.route("/")
def root(query=None):
    return 'go to /search/smth'



@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        
        try:
            with sql.connect("database.db") as con:
                cur = con.cursor()
 
                # Вставляем множество данных в таблицу используя безопасный метод "?"
                albums = [('1', 'test 1'),
                          ('2', 'test 2'),
                          ('3', 'test 3'),
                          ('4', 'test 4')]
 
                cur.executemany("INSERT INTO albums VALUES (?,?)", albums)
            
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from students")
   
    rows = cur.fetchall();

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
