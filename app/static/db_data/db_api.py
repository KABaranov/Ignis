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


def get_user_object(ident):
    user = session.query(User).filter(User.id == ident).first()
    return user

def get_id_from_game(name):
    game = session.query(Game).filter(Game.name == name).first()
    return game.id


def get_games():
    games = {}
    for elem in session.query(Game).all():
        games[elem.id] = elem.name
    return games


def get_user_games(ident):
    games_to_user = session.query(UsersToGames).filter(UsersToGames.id_user == ident).all()
    games = [elem.id_game for elem in games_to_user]
    return games


def add_games_to_user(games, user):
    session.query(UsersToGames).filter(UsersToGames.id_user == user.id).delete()
    for elem in games:
        game = UsersToGames(id_user=user.id, id_game=elem)
        session.add(game)
    session.commit()


def add_team(game, name, owner, link, public):
    team = Team(name=name, owner=owner.id, link=link, public=public)
    session.add(team)
    session.commit()
    team = session.query(Team).filter(Team.name == name).first().id
    game_to_team = TeamsToGames(id_game=game, id_team=team)
    user_to_team = UsersToTeams(id_user=owner.id, id_team=team)
    session.add(user_to_team)
    session.add(game_to_team)
    session.commit()


def team_is_unique(name, link):
    team = session.query(Team).filter((Team.name == name) | (Team.link == link)).first()
    if team:
        return False
    return True


def get_user_teams(ident):
    teams = [session.query(Team).filter(Team.id == elem).first() for elem in [elem.id_team for elem in
                                                                              session.query(UsersToTeams).filter(UsersToTeams.id_user == ident).all()]]
    return teams


def update_profile(user, name, surname, age, city, look_for, about):
    old_user = session.query(User).filter(User.id == user.id).first()
    user = {key: value for key, value in old_user.__dict__.items()
                if key not in ["user", "name", "surname", "age", "city", "look_for", "about", "_sa_instance_state"]}
    new_user = User(name=name, surname=surname, age=age, city=city, look_for=look_for, about=about, **user)
    session.delete(old_user)
    session.add(new_user)
    session.commit()


def get_user_friends(ident):
    friends = [session.query(User).filter(User.id == elem).first() for elem in [elem.id_friend for elem in
                                                                              session.query(UsersToUsers).filter(UsersToUsers.id_user == ident).all()]]
    return friends



