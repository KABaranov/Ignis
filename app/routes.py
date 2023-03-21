from flask import *
from app import app
from app.database import *


@app.route('/test')
def test():
    return render_template('error/500.html', title='Ошибка')


@app.route('/')
def unregistered():
    return render_template('unregistered.html', title='Ignis')


@app.route('/log-in', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not db_log(email, password):
            return render_template('base.html')
        return 'Неправильное имя или пароль'
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
            return 'МНогА'
        return 'Занято'
    return render_template('reg-in.html')