from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from sqlalchemy import desc

from articles.models import Article
from articles.serializers import ArticleListSerializer, ArticleDetailsSerializer
from blog_api.factory import db
from categories.models import Category
from routes import blueprint
from shared.database import get_or_create
from shared.serializers import get_error_response, get_success_response
from tags.models import Tag

article_blueprint = Blueprint('article', __name__)


class ArticleResource(Resource):
    def get(self):
        pass


@blueprint.route('/articles', methods=['GET'])
def list_articles():
    page = request.args.get('page', 1)
    page_size = request.args.get('page', 5)
    # articles = Article.query.order_by(desc(Article.publish_on)).offset(0).limit(page_size).all()
    articles = Article.query.order_by(desc(Article.publish_on)).paginate(page=page, per_page=page_size)
    return jsonify(ArticleListSerializer(articles).get_data()), 200


@blueprint.route('/articles/<article_slug>', methods=['GET'])
def show_article(article_slug):
    article = Article.query.filter_by(slug=article_slug).first()
    # article = Article.query.filter_by(slug=article_slug).first_or_404()
    return jsonify(ArticleDetailsSerializer(article).data), 200


@blueprint.route('/articles/by_id/<article_id>', methods=['GET'])
def by_id(article_id):
    article = Article.query.get(article_id)
    # article = Article.query.filter_by(slug=article_slug).first_or_404()
    return jsonify(ArticleDetailsSerializer(article).data), 200


@blueprint.route('/articles/<article_slug>', methods=['PUT'])
@jwt_required
def update_article(article_slug):
    article = Article.query.filter_by(slug=article_slug).first()
    if article is None:
        return get_error_response(messages='not found', status_code=404)
    title = request.json.get('title')
    if title:
        article.title = title

    description = request.json.get('description')
    if description:
        article.description = description

    body = request.json.get('body')
    if body:
        article.body = body

    tags_input = request.json.get('tags')
    categories_input = request.json.get('categories')
    tags = []
    categories = []
    if categories_input:
        for category in categories_input:
            categories.append(
                get_or_create(db.session, Category, {'description': category.get('description', None)},
                              name=category['name'])[0])

    if tags_input:
        for tag in tags_input:
            tags.append(get_or_create(db.session, Tag, {'description': tag.get('description')}, name=tag['name'])[0])

    article.tags = tags
    article.categories = categories
    db.session.commit()
    response = {'full_messages': ['Article updated successfully']}
    response.update(ArticleDetailsSerializer(article).data)
    return jsonify(response)


@blueprint.route('/articles', methods=['POST'])
@jwt_required()
def create_article():
    user = current_identity
    if user.is_not_author() and user.is_not_admin():
        pass
    title = request.json.get('title')
    description = request.json.get('description')
    body = request.json.get('body')
    tags_input = request.json.get('tags')
    categories_input = request.json.get('categories')
    tags = []
    categories = []
    for category in categories_input:
        categories.append(
            get_or_create(db.session, Category, {'description': category.get('description', None)},
                          name=category['name'])[0])

    for tag in tags_input:
        tags.append(get_or_create(db.session, Tag, {'description': tag.get('description')}, name=tag['name'])[0])

    user_id = user.id

    article = Article(title=title, description=description, body=body, user_id=user_id, tags=tags,
                      categories=categories)
    db.session.add(article)
    db.session.commit()
    response = {'full_messages': ['Article created successfully']}
    response.update(ArticleDetailsSerializer(article).data)
    return jsonify(response)


@blueprint.route('/articles/<article_slug>', methods=['DELETE'])
@jwt_required()
def destroy_article(article_slug):
    article = Article.query.filter_by(slug=article_slug).first()
    db.session.delete(article)
    db.session.commit()
    return get_success_response('Article deleted successfully')


@blueprint.route('/articles/by_id/<article_id>', methods=['DELETE'])
@jwt_required()
def destroy_article_by_id(article_id):
    article = Article.query.get(article_id).first()
    db.session.delete(article)
    db.session.commit()
    return get_success_response('Article deleted successfully')
