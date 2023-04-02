import datetime
import sqlalchemy
from .db_session import *
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    look_for = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)


class Team(SqlAlchemyBase):
    __tablename__ = 'teams'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             unique=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    link = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)


class Game(SqlAlchemyBase):
    __tablename__ = 'games'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             unique=True)

    def __repr__(self):
        return self.name


class UsersToTeams(SqlAlchemyBase):
    __tablename__ = 'users_to_teams'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_team = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('teams.id'))
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    role = sqlalchemy.Column(sqlalchemy.String)


class GameSearchParams(SqlAlchemyBase):
    __tablename__ = 'game_search_params'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_game = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('game.id'))
    parameter = sqlalchemy.Column(sqlalchemy.String)


class TeamsToGames(SqlAlchemyBase):
    __tablename__ = 'teams_to_games'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_team = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('teams.id'))
    id_game = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('game.id'))


class UsersToGames(SqlAlchemyBase):
    __tablename__ = 'users_to_games'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    id_game = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('games.id'))


class UsersToUsers(SqlAlchemyBase):
    __tablename__ = 'users_to_users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    id_friend = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    request_status = sqlalchemy.Column(sqlalchemy.Integer, default=0)
