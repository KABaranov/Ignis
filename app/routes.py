from flask import *
from app import app
from flask_wtf import CSRFProtect
import json

from .decorators import check_confirmed
from .static.db_data.db_api import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from app import confirmation, email

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/log-in'
MAX_FILE_SIZE = 1024 * 1024 + 1


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/test')
def test():
    with open('app/static/json/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    token = confirmation.generate_confirmation_token(current_user.email)
    html = render_template('user/activate.html', confirm_url=token)
    subject = "Подтвердите аккаунт"
    email.send_email(current_user.email, subject, html)
    return render_template('find.html', title='Поиск', cities=cities, gamelist=get_games())


@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('/profile/settings')
    flash('Пожалуйста, подтвердите аккаунт!', 'warning')
    return render_template('user/unconfirmed.html')


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    try:
        user_email = confirmation.confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    confirm_email(user_email)
    return redirect('/')


@app.route('/unconfirmed/resend-confirm')
@login_required
def resend_confirm():
    token = confirmation.generate_confirmation_token(current_user.email)
    html = render_template('user/activate.html', confirm_url=token)
    subject = "Подтвердите аккаунт"
    email.send_email(current_user.email, subject, html)
    return 'Проверьте почту'


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
        user_email = request.form.get('email')
        password = request.form.get('password-1')
        reg = db_reg(nickname, user_email, password)
        if reg == 'SUCCESS':
            token = confirmation.generate_confirmation_token(user_email)
            html = render_template('user/activate.html', confirm_url=token)
            subject = "Подтвердите аккаунт"
            email.send_email(user_email, subject, html)
            return redirect('/unconfirmed')
        elif reg == 'TOO_MANY_SYMBOLS':
            return render_template('reg-in.html', message='Имя пользователя должно быть меньше 15 символов')
        elif reg == 'USER_EXISTS':
            return render_template('reg-in.html', message='Пользователь с таким именем/почтой уже существует')
    return render_template('reg-in.html')


@app.route('/main')
@login_required
@check_confirmed
def main():
    with open('app/static/json/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    return render_template('find.html', title='Поиск', cities=cities, gamelist=get_games())


@app.route('/main/<int:ident>')
@login_required
@check_confirmed
def ident(ident):
    return render_template('main.html', username=get_user_from_id(ident))


@app.route('/profile/choose-game', methods=['GET', 'POST'])
@login_required
@check_confirmed
def choose_game():
    if request.method == 'POST':
        add_games_to_user(request.form.getlist('game'), current_user)
        return redirect(f'/profile/{current_user.id}/games')
    return render_template('choosegame.html', gamelist=get_games(), title='Выбор игр',
                           usergames=get_user_games(current_user.id))


@app.route('/profile/settings', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile_settings():
    with open('app/static/json/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    if request.method == 'POST':
        surname = request.form.get('surname')
        name = request.form.get('name')
        age = request.form.get('age')
        city = request.form.get('city')
        look_for = 1 if request.form.get('look') == '1' else 0
        about = request.form.get('about')
        if name and surname and age and city:
            session.query(User).get(current_user.id).full = 1
            session.commit()
        update_profile(current_user, name, surname, age, city, look_for, about)

        img = request.files['image-load']
        if img.filename:
            file_bytes = img.read()
            if len(file_bytes) < MAX_FILE_SIZE:
                with open(f"app/static/img/profile/{current_user.id}.png", 'wb') as f:
                    f.write(file_bytes)
                session.query(User).get(current_user.id).ico = 1
                session.commit()
            else:
                return 'eeeee'  # TODO Придумать ошибку

        return redirect('/profile/settings')
    return render_template('profile_settings.html', title='Настройка профиля', cities=cities)


@app.route('/delete-profile-img')
@check_confirmed
def background_process_test():
    session.query(User).get(current_user.id).ico = 0
    session.commit()
    try:
        os.remove(f"app/static/img/profile/{current_user.id}.png")
    except BaseException:
        pass
    return 'nothing'


@app.route('/chat')
@login_required
@check_confirmed
def chat():
    return render_template('chat.html', title='Мессенджер')


@app.route('/team/<link>')
@login_required
@check_confirmed
def team_search(link):
    if link.isalpha():
        render_template('')


@app.route('/profile/<int:ident>/games')
@login_required
@check_confirmed
def games(ident):
    return render_template('games.html', nickname=get_user_from_id(ident), usergames=get_user_games(ident),
                           gamelist=get_games(), ident=ident)


@app.route('/profile/<int:ident>/teams')
@login_required
@check_confirmed
def teams(ident):
    return render_template('teams.html', nickname=get_user_from_id(ident),
                           teamlist=get_user_teams(ident), ident=ident)


@app.route('/profile/<int:ident>/friends')
@login_required
@check_confirmed
def friends(ident):
    friendlist = get_user_friends(ident)
    return render_template('friends.html', nickname=get_user_from_id(ident),
                           friendlist=friendlist, ident=ident)


@app.route('/create-team', methods=['GET', 'POST'])
@login_required
@check_confirmed
def create_team():
    if request.method == 'POST':
        name = request.form.get('name')
        link = '-'.join(request.form.get('link').lower().split())
        game = get_id_from_game(request.form.get('game'))
        public = 1 if request.form.get('public') == "1" else 0
        if any(elem.isalpha() for elem in link) and team_is_unique(name, link):
            add_team(game, name, current_user, link, public)
            return redirect(f'/profile/{current_user.id}/teams')
        # TODO придумать ошибку
        return 'придумать ошибку'
    return render_template('create_team.html', gamelist=get_games())


@app.route('/profile/<int:ident>')
@login_required
@check_confirmed
def profile(ident):
    user = get_user_object(ident)
    m = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа',
         'Сентября', 'Октября', 'Ноября', 'Декабря']
    date = f'{user.created_date.day} {m[user.created_date.month - 1]} {user.created_date.year} года'
    return render_template('profile.html', user=user, date=date)
