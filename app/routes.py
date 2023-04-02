from flask import *
from app import app
from flask_wtf import CSRFProtect
import json
from .static.db_data.db_api import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/log-in'


@app.route('/test')
def test():
    with open('app/static/json/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    return render_template('find.html', title='Поиск', cities=cities)


@app.route('/')
def unregistered():
    return render_template('unregistered.html', title='Ignis')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/log-in', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        log, user = db_log(email, password)
        if log == 'SUCCESS':
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else '/main')
        elif log == 'WRONG_PASSWORD_OR_EMAIL':
            return render_template('log-in.html', message='Неправильное имя или пароль')
    return render_template('log-in.html')


@app.route('/log-out')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/reg-in', methods=['POST', 'GET'])
def regin():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        password = request.form.get('password-1')
        reg = db_reg(nickname, email, password)
        if reg == 'SUCCESS':
            return redirect('/log-in')
        elif reg == 'TOO_MANY_SYMBOLS':
            return render_template('reg-in.html', message='Имя пользователя должно быть меньше 15 символов')
        elif reg == 'USER_EXISTS':
            return render_template('reg-in.html', message='Пользователь с таким именем/почтой уже существует')
    return render_template('reg-in.html')


@app.route('/main')
@login_required
def main():
    return render_template('main.html', username=current_user.nickname)


@app.route('/main/<int:ident>')
def ident(ident):
    return render_template('main.html', username=get_user_from_id(ident))


@app.route('/profile/choose-game')
def choose_game():
    gamelist = get_games()
    return render_template('choosegame.html', gamelist=gamelist, title='Игры пользователя')


@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', title='Мессенджер')


@app.route('/team/<link>')
@login_required
def team_search(link):
    if link.isalpha():

        render_template('')

