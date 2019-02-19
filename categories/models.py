from datetime import datetime

from slugify import slugify
from sqlalchemy import event

from blog_api.factory import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(), index=True)
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    def __repr__(self):
        return self.name


articles_categories = db.Table("articles_categories",
                               db.Column("category_id", db.Integer, db.ForeignKey("categories.id")),
                               db.Column("article_id", db.Integer, db.ForeignKey("articles.id")))


@event.listens_for(Category.name, 'set')
def receive_set(target, value, oldvalue, initiator):
    target.slug = slugify(unicode(value))
