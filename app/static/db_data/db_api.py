import flask
from flask import jsonify, request
import hashlib
from . import db_session
from .__all_models import *

db_session.global_init("app/static/db/users.db")
session = db_session.create_session()


def get_all_teams(team_id):
    team = session.query(Team).get(team_id)
    users = session.query(User).join(UsersToTeams).filter(UsersToTeams.id_team == team_id).all()
    return [team.to_dict(), users]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def db_reg(username, email, password):
    if len(username) > 15:
        return 'TOO_MANY_SYMBOLS'
    user = session.query(User).filter((User.email == email) | (User.nickname == username)).first()
    if user:
        return 'USER_EXISTS'
    user = User(nickname=username, email=email, password=hash_password(password))
    session.add(user)
    session.commit()
    return 'SUCCESS'


def db_log(email, password):
    user = session.query(User).filter(User.email == email.lower(), User.password == hash_password(password)).first()
    if not user:
        return 'WRONG_PASSWORD_OR_EMAIL', None
    return 'SUCCESS', user


def get_user_from_id(ident):
    user = session.query(User).filter(User.id == ident).first().__dict__
    return user['nickname']


def get_id_from_game(name):
    game = session.query(Game).filter(Game.name == name).first().__dict__
    return game['id']


def get_games():
    games = {}
    for elem in session.query(Game).all():
        games[elem.__dict__['id']] = elem.__dict__['name']
    return games


def get_user_games(ident):
    games_to_user = session.query(UsersToGames).filter(UsersToGames.id_user == ident).all()
    games = [elem.__dict__['id_game'] for elem in games_to_user]
    return games


def add_games_to_user(games, user):
    session.query(UsersToGames).filter(UsersToGames.id_user == user.id).delete()
    for elem in games:
        game = UsersToGames(id_user=user.id, id_game=elem)
        session.add(game)
    session.commit()


def add_team(game, name, owner, link, public):
    team = Team(name=name, owner=owner, link=link, public=public)
    session.add(team)
    session.commit()
    team = session.query(Team).filter(Team.name == name).first().__dict__['id']
    game_to_team = TeamsToGames(id_game=game, id_team=team)
    session.add(game_to_team)
    session.commit()


def team_is_unique(name, link):
    print(name)
    print(link)
    team = session.query(Team).filter((Team.name == name) | (Team.link == link)).first()
    if team:
        # print(team.__dict__)
        return False
    return True


# def get_user_teams(user):



