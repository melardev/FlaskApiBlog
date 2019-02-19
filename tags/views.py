from flask import request, jsonify
from sqlalchemy import desc

from routes import blueprint
from tags.models import Tag
from tags.serializers import TagListSerializer


@blueprint.route('/tags', methods=['GET'])
def list_tags():
    page_size = request.args.get('page_size', 5)
    page = request.args.get('page', 1)
    tags = Tag.query.order_by(desc(Tag.created_at)).paginate(page=page, per_page=page_size)
    return jsonify(TagListSerializer(tags).get_data()), 200
