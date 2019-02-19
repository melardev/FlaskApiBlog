from datetime import datetime

from slugify import slugify
from sqlalchemy import event
from sqlalchemy.orm import relationship

from blog_api.factory import db
from categories.models import articles_categories
from tags.models import articles_tags


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, unique=True)
    body = db.Column(db.Text)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)
    publish_on = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=db.backref('articles'))

    '''
    liked_by = relationship(
        'user',
        secondary=likesModel,
        backref='likes',
        lazy='dynamic')
    '''

    tags = relationship(
        'Tag', secondary=articles_tags,
        backref='articles')

    categories = relationship(
        'Category', secondary=articles_categories,
        backref='articles')

    # comments = relationship('Comment', backref='article', lazy='dynamic')

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
            return True
        return False

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False

    def __repr__(self):
        return '<Article %r>' % self.body

    def __str__(self):
        return '<Article {}>'.format(self.body)


@event.listens_for(Article.title, 'set')
def receive_set(target, value, oldvalue, initiator):
    target.slug = slugify(unicode(value))
