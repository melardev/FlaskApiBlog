from datetime import datetime

from blog_api.factory import db, bcrypt
from roles.models import users_roles


# from subscriptions.models import user_subscriptions


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Binary(128), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    first_name = db.Column(db.String(300), nullable=False)
    last_name = db.Column(db.String(300), nullable=False)

    roles = db.relationship(
        'Role', secondary=users_roles,
        backref='users')

    '''
    articles = db.relationship('Article',
                               foreign_keys='articles.user_id',
                               backref='user', lazy='dynamic')
    
    comments = db.relationship('Comment',
                               foreign_keys='comments.user_id',
                               backref='user', lazy='dynamic')
    '''

    '''
        following = db.relationship(
            'User', secondary=user_subscriptions,
            primaryjoin=(user_subscriptions.c.follower_id == id),
            secondaryjoin=(user_subscriptions.c.following_id == id),
            backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    '''

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            user_subscriptions.c.followed_id == user.id).count() > 0

    def is_admin_or_author(self):
        return db.session.query(User.id).filter(((User.roles.any(name='ROLE_AUTHOR')) | (User.roles.any(name='ROLE_ADMIN'))) & (User.id==self.id)).count() > 0
        # User.query.filter(User.roles.any(name='ROLE_ADMIN')).all()
        # User.query.join(User.roles).filter_by(genre_id=genre.id).all()

    def is_admin(self):
        return 'ROLE_ADMIN' in [r.name for r in self.roles]

    def is_not_admin(self):
        return not self.is_admin()

    def is_author(self):
        return 'ROLE_AUTHOR' in [r.name for r in self.roles]

    def is_not_author(self):
        return not self.is_author()
