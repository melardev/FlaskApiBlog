from sqlalchemy import UniqueConstraint

from blog_api.factory import db


class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'

    following_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    following = db.relationship("User", foreign_keys=[following_id], backref='follower_subscriptions')
    follower = db.relationship("User", foreign_keys=[follower_id], backref='following_subscriptions')

    __mapper_args__ = {'primary_key': [following_id, follower_id]}
    __table_args__ = (UniqueConstraint('following_id', 'follower_id', name='one_subscription_for_same_user'),)


user_subscriptions = db.Table(
    'user_subscriptions',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('users.id')),
    keep_existing=True
)


class SiteSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
