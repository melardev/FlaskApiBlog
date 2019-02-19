from operator import or_

from flask import jsonify, request
from flask_jwt import current_identity, jwt_required
from sqlalchemy.orm import load_only

from blog_api.factory import db
from routes import blueprint
from shared.serializers import get_success_response, get_error_response, PageSerializer
from subscriptions.models import UserSubscription
from subscriptions.serializers import UserSubscriptionsSerializer
from users.models import User
from users.serializers import UserListSerializer


@blueprint.route('/users/followers', methods=['GET'])
@jwt_required()
def my_followers():
    user = current_identity
    page_size = request.args.get('page_size', 5)
    page = request.args.get('page', 1)
    following_ids = [ur.following_id for ur in
                     UserSubscription.query.filter_by(follower_id=user.id).options(load_only('following_id')).all()]
    following = db.session.query(User).filter(User.id.in_(following_ids)).options(load_only('id', 'username')).paginate(
        page=page, per_page=page_size)
    return jsonify(UserListSerializer('following', following).get_data()), 200


@blueprint.route('/users/subscriptions', methods=['GET'])
@jwt_required()
def my_user_subscriptions():
    user = current_identity
    page_size = request.args.get('page_size', 5)
    page = request.args.get('page', 1)
    user_subscriptions = UserSubscription.query.filter(
        (UserSubscription.follower_id == user.id) | (UserSubscription.following_id == user.id)).all()
    following_ids = []
    follower_ids = []
    for ur in user_subscriptions:
        if ur.following_id == user.id:
            follower_ids.append(ur.follower_id)
        elif ur.follower_id == user.id:
            following_ids.append(ur.following_id)

    users = db.session.query(User).filter(User.id.in_(follower_ids + following_ids)).options(
        load_only('id', 'username')).paginate(page=page, per_page=page_size)

    response = UserSubscriptionsSerializer(users, following_ids, follower_ids).data

    return jsonify(response), 200


@blueprint.route('/users/<username>/followers', methods=['POST'])
@jwt_required()
def follow_user(username):
    user = current_identity
    following = User.query.filter_by(username=username).options(load_only('id')).first()
    if not hasattr(following, 'username'):
        return get_error_response('Permission denied, This user does not exist')
    if following.id == user.id:
        return get_error_response('Permission denied, You can not follow yourself')

    user_subscription = UserSubscription.query.filter_by(following_id=following.id, follower_id=user.id).first()

    if user_subscription is None:
        if following.is_admin_or_author():
            user_subscription = UserSubscription(following_id=following.id, follower_id=user.id)
            db.session.add(user_subscription)
            db.session.commit()
            return get_success_response('You are now following %s' % username)
        else:
            return get_error_response('Permission denied, You can not follow a non author user')
    else:
        return get_error_response('Permission denied, You already following this user')


@blueprint.route('/users/<username>/followers', methods=['DELETE'])
@jwt_required()
def unfollow_user(username):
    user = current_identity
    following = User.query.filter_by(username=username).options(load_only('id')).first()
    if not hasattr(following, 'id'):
        return get_error_response('Permission denied, This user does not exist')

    user_subscription = UserSubscription.query.filter_by(following_id=following.id, follower_id=user.id).first()

    if user_subscription is not None:
        db.session.delete(user_subscription)
        db.session.commit()
        return get_success_response('You are now not following %s' % username)
    else:
        return get_error_response('Permission denied, You are not following this user')
