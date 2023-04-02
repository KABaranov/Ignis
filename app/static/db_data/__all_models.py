import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase):
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

    def __repr__(self):
        return str(self.id)# [self.id, self.nickname, self.email, self.surname, self.name, self.age, self.age, self.city, self.look_for, self.about, self.created_date]


class Team(SqlAlchemyBase, SerializerMixin):
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


class UsersToTeams(SqlAlchemyBase):
    __tablename__ = 'users_to_teams'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_team = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('teams.id'))
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    role = sqlalchemy.Column(sqlalchemy.String)

