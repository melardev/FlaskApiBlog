from comments.serializers import CommentListSerializer
from shared.serializers import PageSerializer


def get_dto(article, include_details=False):
    response = {
        'id': article.id,
        'title': article.title,
        'description': article.description,
        'slug': article.slug,
        'user': {
            'id': article.user_id,
            'username': article.user.username
        },
        'tags': [{'id': tag.id, 'name': tag.name, 'slug': tag.slug} for tag in article.tags],
        'categories': [{
            'id': category.id,
            'name': category.name,
            'slug': category.slug} for category in
            article.categories]
    }

    if include_details:
        response['comments'] = CommentListSerializer(article.comments, include_user=True).data
    else:
        response['comments_count'] = len(article.comments)

    return response


class ArticleListSerializer(PageSerializer):
    resource_name = 'articles'

    def get_dto(self, article):
        return get_dto(article)


class ArticleDetailsSerializer():
    def __init__(self, article):
        self.data = get_dto(article, include_details=True)
