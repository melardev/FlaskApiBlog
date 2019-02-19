from sqlalchemy.orm.collections import InstrumentedList

from shared.serializers import PageSerializer


def get_dto(comment, include_article=False, include_user=False):
    data = {
        'id': comment.id,
        'content': comment.content,
        'created_at': comment.created_at,
    }

    if comment.replied_comment_id is not None:
        data['is_reply'] = True
        data['replied_comment_id'] = comment.replied_comment_id

    if include_article:
        data['article'] = {
            'id': comment.article_id,
            'slug': comment.article.slug,
            'title': comment.article.title
        }
    if include_user:
        data['user'] = {
            'id': comment.user_id,
            'username': comment.user.username
        }
    return data


class CommentListSerializer(PageSerializer):
    resource_name = 'comments'

    def __init__(self, comments_or_pagination, **kwargs):
        if type(comments_or_pagination) == InstrumentedList:
            self.data = [get_dto(comment, **kwargs) for comment in comments_or_pagination]
        else:
            super(CommentListSerializer, self).__init__(comments_or_pagination, **kwargs)

    def get_dto(self, comment, **kwargs):
        return get_dto(comment, **kwargs)


class CommentDetailsSerializer():
    def __init__(self, comment, include_user=True, include_article=True):
        self.data = {'success': True}
        self.data.update(comment.get_summary(include_article, include_user))
