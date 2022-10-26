from flask_login import UserMixin
from apps import sqlalchemy, login_manager, mongo
from apps.authentication.util import hash_pass
from datetime import datetime


### Sql
# class Users(sqlalchemy.Model, UserMixin):

#     __tablename__ = 'Users'

#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
#     username = sqlalchemy.Column(sqlalchemy.String(64), unique=True)
#     email = sqlalchemy.Column(sqlalchemy.String(64), unique=True)
#     password = sqlalchemy.Column(sqlalchemy.LargeBinary)

#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]

#             if property == 'password':
#                 value = hash_pass(value)  # we need bytes here (not plain str)

#             setattr(self, property, value)

#     def __repr__(self):
#         return str(self.username)


class Users(mongo.Document, UserMixin):

    id = mongo.IntField(primary_key=True)
    username = mongo.StringField(required=True, unique=True)
    email = mongo.StringField(unique=True)
    password = mongo.StringField(required=True)
    create_date = mongo.DateTimeField()
    modified_date = mongo.DateTimeField(default=datetime.now())

    def __init__(self, **kwargs):
        for property, value in kwargs.items():

            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.objects(id=id).first()
    # return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
