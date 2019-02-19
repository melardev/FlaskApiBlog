from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from blog_api.factory import db


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=db.backref('likes'))

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    article = relationship('Article', backref=db.backref('likes'))

    __mapper_args__ = {'primary_key': [user_id, article_id]}
    __table_args__ = (UniqueConstraint('user_id', 'article_id', name='one_like_per_article_and_user'),)


likesTable = db.Table('likes',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
                      keep_existing=True)
