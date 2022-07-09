from flask import render_template, Flask, g
from config import *
import sqlite3


app = Flask('__name__')
app.config.from_object(testingConfig)
app.config.from_envvar( 'FLASKR_SETTINGS' , silent=True)


def connect_db():
    con = sqlite3.connect('/main-flask-core/user.db')
    
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('/main-flask-core/shem.sql','r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqllite_db = connect_db()
        return g.sqlite_db


@app.teardown_appcontext
def close_db():
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()
        


@app.route('/')
def start(name='grigorii'):
    return render_template('index.html',name)

# @app.route('/home/')
# def home


if __name__ == '__main__':
    app.run()