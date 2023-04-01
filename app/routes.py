from flask import *
from app import app
from app.database import *
from flask_wtf import CSRFProtect
import json

csrf = CSRFProtect(app)


@app.route('/test')
def test():
    with open('app/static/json/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    return render_template('find.html', title='Поиск', cities=cities)


@app.route('/')
def unregistered():
    return render_template('unregistered.html', title='Ignis')


@app.route('/log-in', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not db_log(email, password):
            return redirect('/main')
        return render_template('log-in.html', message='Неправильное имя или пароль')
    return render_template('log-in.html')


@app.route('/reg-in', methods=['POST', 'GET'])
def regin():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        password = request.form.get('password-1')
        reg = db_reg(nickname, email, password)
        if not reg:
            return render_template('base.html')
        elif reg == 'TOO_MANY_SYMBOLS':
            return render_template('reg-in.html', message='Имя пользователя должно быть меньше 15 символов')
        return render_template('reg-in.html', message='Пользователь с таким именем/почтой уже существует')
    return render_template('reg-in.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/profile/choose-game')
def choose_game():
    # TODO: связать gamelist с бд
    gamelist = {0: 'CS:GO', 1: 'Dota 2', 2: 'Rocket League', 3: 'Overwatch', 4: 'Minecraft', 5: 'Civilization VI',
                6: 'HOI IV'}
    return render_template('choosegame.html', gamelist=gamelist, title='Игры пользователя')


@app.route('/chat')
def chat():
    return render_template('chat.html', title='Мессенджер')
