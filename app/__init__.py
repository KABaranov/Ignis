from flask import *
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '$21aA9@1a4DZ&Z?dV02'
csrf = CSRFProtect(app)

from app import routes, errors
