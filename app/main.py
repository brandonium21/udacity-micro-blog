from flask import Flask
from flask import render_template, url_for, request, redirect
from Models import Author, Post, Comment
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

def get_item(key=None):
    return key.get()

@app.route('/', methods=['GET','POST'])
def show_allpost():
    """Return a friendly HTTP greeting."""
    logout = login = None
    user = users.get_current_user()
    posts = Post.query().fetch()
    print posts
    if users.get_current_user():
        logout = users.create_logout_url(users.create_login_url(request.url))
    else:
        login = users.create_login_url(request.url)

    return render_template("allpost.html", 
        posts=posts, user=user, get_item=get_item,
        logout=logout, login=login)


@app.route('/editPost', methods=['GET','POST'])
@login_needed
def edit_post():
    """Return a friendly HTTP greeting."""
    if request.method == 'POST':
        title = request.form['title']
        post_id = request.form['post_id']
        content = request.form['content']
        post = ndb.Key(Post, int(post_id)).get()
        if post.author == users.get_current_user():
            post.title = title
            post.content = content
            post.updated_on = datetime.datetime.now()
            post.put()
            time.sleep(.2)
            return redirect(url_for("show_allpost"))
        return render_template('unauthorized.html')


@app.route('/deletePost/<post_key>', methods=['GET','POST'])
@login_needed
def del_post(post_key):
    """Return a friendly HTTP greeting."""
    del_post = ndb.Key(Post, int(post_key))
    if post.author == users.get_current_user():
        del_post.delete()
        time.sleep(.2)
        return redirect(url_for("show_allpost"))
    return render_template('unauthorized.html')


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


@app.route('/addcomment', methods=['GET', 'POST'])
@login_needed
def show_addcomment():
    """Return a friendly HTTP greeting."""
    if request.method == 'POST':
        post = ndb.Key(Post, int(request.form['post_id'])).get()
        cmt = Comment(
            content = request.form['content'],
            author = users.get_current_user())
        cmt.put()
        post.comments.append(cmt.key)
        post.put()
        time.sleep(.2)
        return redirect(url_for("show_allpost"))
    #return redirect(url_for("show_allpost", user=users.get_current_user()))

@app.route('/like/<post>', methods=['GET','POST'])
@login_needed
def like(post):
    post = ndb.Key(Post, int(post)).get()
    if post.author == users.get_current_user():
        return render_template('unauthorized.html')
    if users.get_current_user() in post.likes:
        return redirect(url_for("show_allpost"))
    post.likes.append(users.get_current_user())
    post.put()
    time.sleep(.2)
    return redirect(url_for("show_allpost"))
    

@app.route('/unlike/<post_key>', methods=['GET','POST'])
@login_needed
def unlike(post_key):
    post = ndb.Key(Post, int(post_key)).get()
    if post.author == users.get_current_user():
        return render_template('unauthorized.html')
    if users.get_current_user() in post.likes:
        indx = post.likes.index(users.get_current_user())
        del post.likes[indx]
        post.put()
        time.sleep(.2)
    return redirect(url_for("show_allpost"))
        

@app.route('/editComment', methods=['GET','POST'])
@login_needed
def edit_comment():
    """Return a friendly HTTP greeting."""
    if request.method == 'POST':
        cmt_id = request.form['cmt_key']
        content = request.form['content']
        cmt = ndb.Key(Comment, int(cmt_id)).get()
        if cmt.author == users.get_current_user():
            cmt.content = content
            cmt.put()
            time.sleep(.2)
            return redirect(url_for("show_allpost"))
        return render_template('unauthorized.html')


@app.route('/deleteCmt/<comment_key>', methods=['GET','POST'])
@login_needed
def del_comment(comment_key):
    """Return a friendly HTTP greeting."""
    del_comment = ndb.Key(Comment, int(comment_key))
    if comment.author == users.get_current_user():
        del_comment.delete()
        time.sleep(.2)
        return redirect(url_for("show_allpost"))
    return render_template('unauthorized.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template("404_page.html"), 404
