from flask import *
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from database import *


app = Flask(__name__)
# TODO: Перенести в переменное окружение
app.config['SECRET_KEY'] = '$21aA9@1a4DZ&Z?dV02'
csrf = CSRFProtect(app)


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


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
