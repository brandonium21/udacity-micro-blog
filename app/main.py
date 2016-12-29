from flask import Flask
from flask import render_template, url_for, request, redirect
from Models import Author, Post
from util import login_needed
from werkzeug.security import generate_password_hash, check_password_hash
from google.appengine.ext.db.metadata import Property
from google.appengine.ext import ndb
from app import app
from google.appengine.api import users
import time
import datetime


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/', methods=['GET','POST'])
def show_allpost():
    """Return a friendly HTTP greeting."""
    logout = login = None
    user = users.get_current_user()
    posts = Post.query()
    if users.get_current_user():
        logout = users.create_logout_url(request.url)
    else:
        login = users.create_login_url(request.url)

    return render_template("allpost.html", 
        posts=posts, user=user, 
        logout=logout, login=login)

@app.route('/editPost', methods=['GET','POST'])
def edit_post():
    """Return a friendly HTTP greeting."""
    if request.method == 'POST':
        title = request.form['title']
        post_id = request.form['post_id']
        content = request.form['content']
        post = ndb.Key(Post, int(post_id)).get()
        post.title = title
        post.content = content
        post.updated_on = datetime.datetime.now()
        post.put()
        time.sleep(.2)
        return redirect(url_for("show_allpost"))

@app.route('/deletePost/<post_key>', methods=['GET','POST'])
def del_post(post_key):
    """Return a friendly HTTP greeting."""
    del_post = ndb.Key(Post, int(post_key)).delete()
    time.sleep(.2)
    return redirect(url_for("show_allpost"))


@app.route('/addpost', methods=['GET', 'POST'])
@login_needed
def show_addpost():
    """Return a friendly HTTP greeting."""
    if request.method == 'POST':
        title = request.form['title']
        if not request.form['title']:
            title = "No Title"
        post = Post(
            title = title, 
            content = request.form['content'],
            author = users.get_current_user())
        post.put()
        time.sleep(.2)
        return redirect(url_for("show_allpost"))
    #return redirect(url_for("show_allpost", user=users.get_current_user()))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template("404_page.html"), 404
