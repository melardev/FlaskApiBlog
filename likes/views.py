from flask import request, jsonify
from flask_jwt import jwt_required, current_identity
from sqlalchemy import desc
from sqlalchemy.orm import load_only

from articles.models import Article
from articles.serializers import ArticleListSerializer
from blog_api.factory import db
from likes.models import Like
from routes import blueprint
from shared.serializers import get_error_response, get_success_response


@blueprint.route('/<article_slug>/likes')
def get_article_likes(article_slug):
    article_id = Article.query.filter(slug=article_slug).with_entities('id')
    Like.query.filter_by(article_id=article_id)


@blueprint.route('/likes')
@jwt_required()
def my_likes():
    page = request.args.get('page', 1)
    page_size = request.args.get('page', 5)
    user = current_identity
    articles = Article.query.order_by(desc(Article.publish_on)).filter(
        Article.likes.any(Like.user_id == user.id)).paginate(page=page, per_page=page_size)
    return jsonify(ArticleListSerializer(articles).get_data()), 200


@blueprint.route('/articles/<article_slug>/likes', methods=['POST'])
@jwt_required()
def like_article(article_slug):
    user = current_identity
    article = Article.query.filter_by(slug=article_slug).options(load_only('id', 'title')).first()

    if Like.query.filter_by(article_id=article.id, user_id=user.id).count() == 0:
        like = Like(article_id=article.id, user_id=user.id)
        db.session.add(like)
        db.session.commit()
        return get_success_response('You are now liking %s' % article.title)
    else:
        return get_error_response('Permission denied, You already liked this article')


@blueprint.route('/articles/<article_slug>/likes', methods=['DELETE'])
@jwt_required()
def unlike(article_slug):
    user = current_identity
    article = Article.query.filter_by(slug=article_slug).options(load_only('id', 'title')).first()
    like = Like.query.filter_by(article_id=article.id, user_id=user.id).first()
    if like is not None:
        db.session.delete(like)
        db.session.commit()
        return get_success_response('You have just successfully disliked the article: %s' % article.title)
    else:
        return get_error_response('Permission denied, You are not liking this article')
