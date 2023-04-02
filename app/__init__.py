from flask import *
from flask_wtf import CSRFProtect
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

from app import routes, errors
