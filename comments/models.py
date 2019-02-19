import datetime as dt

from sqlalchemy.orm import relationship

from blog_api.factory import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='comments')

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    article = relationship('Article', backref=db.backref('comments'))

    replied_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    replies = relationship("Comment", backref=db.backref('reply', remote_side=[id]))


