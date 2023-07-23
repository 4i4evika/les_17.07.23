import sqlite3
import os

from flask import Flask, render_template, request, flash, url_for

from DataBase import DataBase

DATABASE = '/tmp/ck.db'
DEBUG = True
SECRET_KEY = '8rd8fhd4u93wehjfergjntr5yg8ty8jmr8cxgs67eaerfet4d'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({'DATABASE': os.path.join(app.root_path, 'ck.db')})


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with open('create_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

# menu = [
#     {'name': 'Главная', 'url': 'index'},
#     {'name': 'Галерея', 'url': 'gallery'},
#     {'name': 'Услуги и цены', 'url': 'price'},
#     {'name': 'Обратная связь', 'url': 'contacts'},
# ]


@app.route('/index')
@app.route('/')
def index():
    db_con = connect_db()
    dbase = DataBase(db_con)
    return render_template('index.html', title='Главная',
                           menu=dbase.get_objects('mainmenu'),
                           posts=dbase.get_objects('posts'))


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    db_con = connect_db()
    dbase = DataBase(db_con)
    if request.method == 'POST':
        if len(request.form['title']) < 3 or len(request.form['text']) < 10:
            flash('Ошибка добавления статьи!', category='error')
        else:
            res = dbase.add_post(request.form['title'], request.form['text'])
            if res:
                flash('Статья успешно добавлена!', category='success')
            else:
                flash('Ошибка добавления статьи!', category='error')

    return render_template('add_post.html', title='Добавить информацию',
                           menu=dbase.get_objects('mainmenu'))

@app.route('/gallery')
def gallery():
    db_con = connect_db()
    dbase = DataBase(db_con)
    return render_template('gallery.html', title='Галерея', menu=dbase.get_objects('mainmenu'))


@app.route('/price')
def price():
    db_con = connect_db()
    dbase = DataBase(db_con)
    return render_template('price.html', title='Услуги и цены', menu=dbase.get_objects('mainmenu'),
                                                                posts=dbase.get_objects('posts1'))


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    db_con = connect_db()
    dbase = DataBase(db_con)
    if request.method == 'POST':
        if len(request.form['username']) >= 3:
            flash('Сообщение отправлено успешно!', category='success')
        else:
            flash('Ошибка отправки!', category='error')
        print(request.form)
        context = {
            'username': request.form['username'],
            'email': request.form['email'],
            'message': request.form['message']
        }
        return render_template('contacts.html', title='Обратная связь', menu=dbase.get_objects('mainmenu'), **context)

    return render_template('contacts.html', title='Обратная связь', menu=dbase.get_objects('mainmenu'))


if __name__ == '__main__':
    create_db()
    app.run()
