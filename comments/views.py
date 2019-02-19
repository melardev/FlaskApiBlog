from flask import request, jsonify
from flask_jwt import jwt_required

from sqlalchemy import desc

from articles.models import Article
from comments.models import Comment
from comments.serializers import CommentListSerializer, CommentDetailsSerializer
from routes import blueprint
from shared.serializers import get_success_response, get_error_response


@blueprint.route('/articles/<article_slug>/comments', methods=['GET'])
def list_comments(article_slug):
    page_size = request.args.get('page_size', 5)
    page = request.args.get('page', 1)
    article_id = Article.query.filter_by(slug=article_slug).with_entities('id').first()[0]
    comments = Comment.query.filter_by(article_id=article_id).order_by(desc(Comment.created_at)).paginate(page=page,
                                                                                                          per_page=page_size)
    return jsonify(CommentListSerializer(comments, include_user=True).get_data()), 200


@blueprint.route('/comments/<comment_id>', methods=['GET'])
def show_comment(comment_id):
    comment = Comment.query.get(comment_id)
    return jsonify(CommentDetailsSerializer(comment).data), 200


@blueprint.route('/articles/<article_slug>/comments', methods=['POST'])
@jwt_required()
def create_comment(article_slug):
    content = request.json.get('content')
    claims = get_jwt_claims()
    user_id = claims.get('id')
    article_id = db.session.query(Article.id).filter_by(slug=article_slug).first()[0]
    comment = Comment(content=content, user_id=user_id, article_id=article_id)

    db.session.add(comment)
    db.session.commit()

    return get_success_response(data=CommentDetailsSerializer(comment).data, messages='Comment created successfully')


@blueprint.route('/comments/<comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment is None:
        return get_error_response(messages='not found', status_code=404)
    content = request.json.get('content')
    if content:
        comment.content = content

    db.session.commit()
    return get_success_response(data=CommentDetailsSerializer(comment).data, messages='Comment updated successfully')


@blueprint.route('/comments/<comment_id>', methods=['DELETE'])
@jwt_required()
def destroy_comment(comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return get_success_response('Comment deleted successfully')
