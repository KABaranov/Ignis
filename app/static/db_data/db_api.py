import flask
from flask import jsonify, request
import hashlib
from . import db_session
from .__all_models import *

db_session.global_init("app/static/db/users.db")


def get_all_teams(team_id):
    db_sess = db_session.create_session()
    team = db_sess.query(Team).get(team_id)
    users = db_sess.query(User).join(UsersToTeams).filter(UsersToTeams.id_team == team_id).all()
    return [team.to_dict(), users]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def db_reg(username, email, password):
    if len(username) > 15:
        return 'TOO_MANY_SYMBOLS'
    session = db_session.create_session()
    user = session.query(User).filter((User.email == email) | (User.nickname == username)).first()
    if user:
        return 'USER_EXISTS'
    user = User(nickname=username, email=email, password=hash_password(password))
    session.add(user)
    session.commit()
    return 'SUCCESS'


def db_log(email, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email.lower(), User.password == hash_password(password)).first()
    if not user:
        return 'WRONG_PASSWORD_OR_EMAIL', None
    return 'SUCCESS', user


def get_user_from_id(ident):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == ident).first().__dict__
    return user['nickname']


def get_games():
    session = db_session.create_session()
    games = {}
    for elem in session.query(Game).all():
        games[elem.__dict__['id']] = elem.__dict__['name']
    return games

