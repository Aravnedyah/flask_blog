import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

#connect to created db and convert to dictionary rows and returned
def get_db_connection():
    conn=sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

#receive an id parameter, call db, post new data. If no post, call 404 error and return post
def get_post(post_id):
    conn=get_db_connection()
    post=conn.execute('SELECT * FROM posts WHERE id=?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

#initiate app and create secret key
app = Flask(__name__)
app.secret_key= 'sdfasdf9sdf0sdf909f0d9fsdfs-098765456#@$@#$(@*dfsdfjsdhfksdfjsdkfew3412iiacuwer12endi12edbasd'

# @app.route() is directing the view. call db, get all posts and return them.
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

#view directs to about page. renders about page
@app.route('/about')
def about():
    return render_template('about.html')

#generates all posts on index page
@app.route('/<int:post_id>')
def post(post_id):
    post=get_post(post_id)
    return render_template('post.html', post=post)

#viewer directs to create.html 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title=request.form['title']
        content=request.form['content']

        if not title:
            flash('Title is Required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                            (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is Required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title= ?, content = ?'
                            ' WHERE id = ?',
                            (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted'.format(post['title']))
    return redirect(url_for('index'))