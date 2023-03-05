from flask import *
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = '$21aA9@1a4DZ&Z?dV02'


@app.route('/')
def unregistered():
    return render_template('unregistered.html', title='Ignis')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
