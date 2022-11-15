from flask_login import UserMixin
from apps import login_manager, mongo
from datetime import datetime


class Users(mongo.Document, UserMixin):

    username = mongo.StringField(required=True, unique=True)
    email = mongo.StringField(unique=True)
    password = mongo.BinaryField(required=True)
    role = mongo.StringField(default='user')
    creation_date = mongo.DateTimeField()
    modified_date = mongo.DateTimeField(default=datetime.now())

    meta = {
        'indexes': [
            'username',
            'email',
            'role',
            'creation_date',
            'modified_date'
        ]
    }

    def save(self, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        self.modified_date = datetime.now()
        return super(Users, self).save(**kwargs)


class Roles(mongo.Document, UserMixin):

    role = mongo.StringField(required=True, unique=True)
    role_name = mongo.StringField(unique=True)
    
    creation_date = mongo.DateTimeField()
    modified_date = mongo.DateTimeField(default=datetime.now())

    meta = {
        'indexes': [
            'role',
            'creation_date',
            'modified_date'
        ]
    }

    def save(self, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        self.modified_date = datetime.now()
        return super(Users, self).save(**kwargs)



@login_manager.user_loader
def user_loader(id):
    return Users.objects(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.objects(username=username).first()
    return user if user else None
