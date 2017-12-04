from flask import Flask, redirect, url_for, \
				  request, render_template, json
from pymongo import MongoClient
import pymongo
import os
import socket
import sys
from bson import ObjectId



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


client = MongoClient('mongodb://backend:27018/dockerdemo')
db = client.blogpostDB

app = Flask(__name__)

@app.route("/")
def landing_page():
    posts = get_all_posts()
    
    return render_template('blog.html', posts=json.loads(posts), post={})


@app.route('/add_post', methods=['POST'])
def add_post():

    new()
    return redirect(url_for('landing_page'))


@app.route('/remove_all')
def remove_all():
    db.blogpostDB.delete_many({})

    return redirect(url_for('landing_page'))


@app.route('/edit_post', methods=['POST'])
def edit_post():
    post_id = request.form['id']

    _post = db.blogpostDB.find_one({'_id':ObjectId(post_id)})
    _post = JSONEncoder().encode(_post)

    return render_template('blog.html', edit=True, post=json.loads(_post))

@app.route('/delete_post', methods=['POST'])
def delete_post():
    delete()
    return redirect(url_for('landing_page'))


## Services

@app.route("/posts", methods=['GET'])
def get_all_posts():
    
    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]
    return JSONEncoder().encode(posts)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'title': request.form['title'],
        'post': request.form['post']
    }
    db.blogpostDB.insert_one(item_doc)

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    return JSONEncoder().encode(posts[-1])


@app.route('/edit', methods=['POST'])
def edit():
    
    post_id = request.form['id']
    item = {
        'title': request.form['title'],
        'post': request.form['post']
    }

    db.blogpostDB.find_one_and_replace({'_id':ObjectId(post_id)}, item)
    return redirect(url_for('landing_page'))


@app.route('/delete', methods=['POST'])
def delete():

    post_id = request.form['id']
    post = db.blogpostDB.delete_one({'_id':ObjectId(post_id)})

    return redirect(url_for('landing_page'))

### Insert function here ###



############################



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
