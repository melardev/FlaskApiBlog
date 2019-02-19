from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, Column
from sqlalchemy.sql import ColumnElement

from blog_api.factory import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=True)


class UserRole(db.Model):
    __tablename__ = 'users_roles'

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    # users = db.relationship("User", foreign_keys=[user_id], backref='roles')
    user = db.relationship("User", foreign_keys=[user_id], backref='users_roles')
    role = db.relationship("Role", foreign_keys=[role_id], backref='users_roles')

    __mapper_args__ = {'primary_key': [user_id, role_id]}
    __table_args__ = (UniqueConstraint('user_id', 'role_id', name='same_role_for_same_user'),)


users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    keep_existing=True
)
