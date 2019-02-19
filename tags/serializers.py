from shared.serializers import PageSerializer


def get_dto(tag, **kwargs):
    return {
        'id': tag.id,
        'name': tag.name,
        'slug': tag.slug
    }


class TagListSerializer(PageSerializer):
    resource_name = 'tags'

    def get_dto(self, tag, **kwargs):
        return get_dto(tag, **kwargs)
