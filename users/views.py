from flask import request, jsonify

from blog_api.factory import db, bcrypt
from roles.models import Role
from routes import blueprint
from .models import User


def token_revoked():
    return jsonify({'success': False, 'full_messages': ['Revoked token']})


def invalid_token_loader(error_message):
    return jsonify({'success': False, 'full_messages': [error_message]})


@blueprint.route('/users', methods=['POST'])
def register():
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    email = request.json.get('email', None)
    role = db.session.query(Role).filter_by(name='ROLE_USER').first()
    db.session.add(
        User(first_name=first_name, last_name=last_name, username=username,
             password=bcrypt.generate_password_hash(password).decode('utf-8'), roles=[role], email=email)
    )
    db.session.commit()
    return jsonify({'success': True, 'full_messages': ['User registered successfully']}), 200


def partially_protected():
    # If no JWT is sent in with the request, get_jwt_identity()
    # will return None
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(logged_in_as=current_user), 200
    else:
        return jsonify(loggeed_in_as='anonymous user'), 200
