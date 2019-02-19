import flask_jwt
from flask import jsonify

from blog_api.factory import app
from users.models import User

'''
Flask-JWT __init__.py has the CONFIG_DEFAULTS which are config keys
'''
'''
This is called to authenticate, it is like the view
'''


# @jwt.authentication_handler
def authentication_handler(username, password):
    # user = User.query.filter_by(username=username).first()
    user = User.query.filter(User.username == username).scalar()
    if user.check_password(password):
        return user


jwt = flask_jwt.JWT(app, authentication_handler=authentication_handler)


# jwt.authentication_handler(authentication_handler)


# jwt.auth_response_callback(jwt_response_handler)


def jwt_error_handler(error):
    return jsonify({'success': False, 'full_messages': [str(error)]}), 400


# this will generate the JWT token(not the response) but the token that will be encoded
# @jwt.identity_handler
def payload_handler(identity):
    result = flask_jwt._default_jwt_payload_handler(identity)
    result.update(
        {'user_id': identity.id, 'username': identity.username, 'roles': [role.name for role in identity.roles]})
    return result


'''
Called when there is an incoming request and the jwt has to be validated,
we receive as argument the decoded jwt payload, we know the jwt is signed with the key, now we make 
the second step, which is to check if the user actually exists.
'''


def identity_handler(decoded_payload):
    user_id = decoded_payload.get('user_id', None)
    if user_id is None:
        return None
    user = User.query.get(user_id)
    return user


jwt.identity_handler(identity_handler)

jwt.jwt_error_handler(jwt_error_handler)
jwt.jwt_payload_handler(payload_handler)


def jwt_response_handler(jwt_token, identity):
    '''
    :param jwt_token: is the result of encoding the returned dict from payload_handler()
    :param identity: is the result of authentication_handler
    :return:
    '''
    return jsonify({'success': True,
                    'token': jwt_token.decode('utf-8'),
                    'user': {
                        'id': identity.id,
                        'username': identity.username,
                        'roles': [role.name for role in identity.roles]
                    }
                    })


jwt.auth_response_handler(jwt_response_handler)
