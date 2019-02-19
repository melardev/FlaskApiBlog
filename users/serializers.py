from sqlalchemy.orm.collections import InstrumentedList

from shared.serializers import PageSerializer


def get_dto(user):
    response = {
        'id': user.id,
        'username': user.username,
    }

    return response


class UserListSerializer(PageSerializer):
    resource_name = 'users'

    def __init__(self, resources_name, paginationobj_or_list, **kwargs):
        self.resource_name = resources_name
        if type(paginationobj_or_list) == list:
            self.data = [get_dto(user, **kwargs) for user in paginationobj_or_list]
        else:
            super(UserListSerializer, self).__init__(paginationobj_or_list, **kwargs)

    def get_data(self):
        return self.data

    def get_dto(self, user):
        return get_dto(user)


class UserDetailsSerializer():
    def __init__(self, user):
        self.data = get_dto(user)
