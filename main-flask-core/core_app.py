from importlib.resources import path
from ntpath import join
from flask import redirect, render_template, Flask, g, abort, flash, url_for,request,session
import sqlite3
import os


app = Flask(__name__)
app.config.from_object(__name__)

# conf
app.config.update(dict(
    SECRET_KEY = 'key',
    DEBUG = True,
    TESTING = True,
    DATABASE = os.path.join(app.root_path,'user.db'),
    USERNAME = 'admin',
    PASSWORD = 'default',
))

app.config.from_envvar( 'FLASKR_SETTINGS' , silent=True)


def connect_db():

    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row

    return con


def init_db():

    with app.app_context():
        db = get_db()

        with app.open_resource('shem.sql','r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():

    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
        return g.sqlite_db


@app.teardown_appcontext
def close_db(error):

    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()
        

@app.route('/')
def show_entries():

    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT title, text FROM entries ORDER BY id DESC')
    entries = cur.fetchall()

    return render_template('show_entries.html',entries = entries)


@app.route('/add', methods=['POST'])
def add_entry():

    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('INSERT INTO entries (title,text) VALUES(?,?)',[request.form['title'],request.form['text']])
    db.commit()
    flash('Новый пост был добавлен)')

    return redirect(url_for('show_entries'))


@app.route('/login',methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':

        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:

            error = 'Неверный логин или пароль'

        else:

            session['logged_in'] = True
            flash('Вы вошли')

            return redirect(url_for('show_entries'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():

    session.pop('logged_in',None)
    flash('Вы вышли из аккаунта')

    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()