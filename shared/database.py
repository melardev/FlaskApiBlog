from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql import ClauseElement

# Alias common SQLAlchemy names
from blog_api.factory import db

Column = db.Column
relationship = relationship
Model = db.Model


class TimeStampedModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime())

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True
