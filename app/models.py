# flask
from flask import current_app
from flask.ext.login import UserMixin
# other
from werkzeug.security import generate_password_hash, check_password_hash
# local
from . import db, login_manager

# Role object communicates with database
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
   
    # function to establish role permissions
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.EDIT, True),
            # the moderator role isn't currently used, but it could be useful int the future to distinguish admins (can do everything) from moderators (can approve claims)
            'Moderator': (Permission.EDIT |
                          Permission.APPROVE, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
        
class Permission: 
    EDIT = 0x01
    APPROVE = 0x02
    ADMINISTER = 0x80

# User object communicates with the database to extract user id,
#  email, username, role_id and password_hash
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    full_name = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions 
    
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    # generate hash from given password to store in DB
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # compare hashed password to password argument
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
    def __init__(self, **kwargs): 
        super(User, self).__init__(**kwargs) 
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    username = db.Column(db.String(64))
    submit_date = db.Column(db.String(64))
    purchase_date = db.Column(db.String(64))
    description = db.Column(db.String(64))
    vendor = db.Column(db.String(64))
    amount = db.Column(db.String(64))
    account = db.Column(db.Integer())
    receipt = db.Column(db.String(64))
    approved = db.Column(db.Integer())
    
    # approve expense
    def approve(self, password):
        self.approved = True
        
    def __repr__(self):
        return '<Expense %r>' % self.id
        
class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def load_expenses(user_id):
    return Expense.query.get(int(user_id))