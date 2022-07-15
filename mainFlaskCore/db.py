from sqlite3 import *

def add_user(username, password):
    db = connect('mainFlaskCore/entr.db')
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        login TEXT,
        password TEXT)''')
    db.commit()
    cur.execute('INSERT INTO users VALUES(?,?)',(username,password))   
    db.commit()

def get_user_data(username,password):
    db = connect('mainFlaskCore/entr.db')
    cursor = db.cursor()
    for i in cursor.execute('SELECT login,password FROM users'):
        if username == i[0] and password == i[1]:
            return True
    
    return False
            
        