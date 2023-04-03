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


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/test')
def test():
    with open('app/static/json/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    return render_template('find.html', title='Поиск', cities=cities, gamelist=get_games())


@app.route('/')
def unregistered():
    return render_template('unregistered.html', title='Ignis')


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
    with open('app/static/json/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    return render_template('find.html', title='Поиск', cities=cities, gamelist=get_games())


@app.route('/main/<int:ident>')
@login_required
def ident(ident):
    return render_template('main.html', username=get_user_from_id(ident))


@app.route('/profile/choose-game', methods=['GET', 'POST'])
@login_required
def choose_game():
    if request.method == 'POST':
        # TODO: Связать лист с БД user-game
        add_games_to_user(request.form.getlist('game'), current_user)
        return redirect(f'/profile/{current_user.id}/games')
    return render_template('choosegame.html', gamelist=get_games(), title='Выбор игр', usergames=get_user_games(current_user.id))


@app.route('/profile/settings', methods=['GET', 'POST'])
@login_required
def profile_settings():
    with open('app/static/json/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    if request.method == 'POST':
        # TODO: Связать лист с БД user
        print(request.form.get('surname'))
        print(request.form.get('name'))
        print(request.form.get('age'))
        print(request.form.get('city'))
        if request.form.get('look') == '1':
            print(1)
        else:
            print(0)
        return redirect('/main')
    return render_template('profile_settings.html', title='Настройка профиля', cities=cities)


@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', title='Мессенджер')


@app.route('/team/<link>')
@login_required
def team_search(link):
    if link.isalpha():
        render_template('')


@app.route('/profile/<int:ident>/games')
@login_required
def games(ident):
    return render_template('games.html', nickname=get_user_from_id(ident), usergames=get_user_games(ident),
                           gamelist=get_games(), ident=ident)


@app.route('/profile/<int:ident>/teams')
@login_required
def teams(ident):
    # TODO передавать список команд пользователя сюда (Передавать объекты, а не названия)
    teamlist = [1,  2, 3, 4, 5]
    return render_template('teams.html', nickname=get_user_from_id(ident),
                           teamlist=teamlist, ident=ident)


@app.route('/profile/<int:ident>/friends')
@login_required
def friends(ident):
    # TODO передавать список друзей пользователя сюда  (Передавать объекты, а не названия)
    friendlist = [2, 3]
    return render_template('friends.html', nickname=get_user_from_id(ident),
                           friendlist=friendlist, ident=ident)


@app.route('/create-team', methods=['GET', 'POST'])
@login_required
def create_team():
    if request.method == 'POST':
        name = request.form.get('name')
        link = '-'.join(request.form.get('link').lower().split())
        game = get_id_from_game(request.form.get('game'))
        public = 1 if request.form.get('public') == "1" else 0
        # print(any(elem.isalpha() for elem in link))
        # print(team_is_unique(name, link))
        if any(elem.isalpha() for elem in link) and team_is_unique(name, link):
            add_team(game, name, current_user.id, link, public)
            return redirect(f'/profile/{current_user.id}/teams')
        return 'придумать ошибку'
    return render_template('create_team.html', gamelist=get_games())