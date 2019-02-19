from shared.serializers import PageSerializer
from users.serializers import UserListSerializer


class UserSubscriptionsSerializer():
    def __init__(self, user_pagination_obj, following_ids, follower_ids):
        self.data = {}
        self.data['page_meta'] = PageSerializer(user_pagination_obj, serialize_items=False).data
        followers = []
        following = []
        for u in user_pagination_obj.items:
            if u.id in follower_ids:
                followers.append(u)
            elif u.id in following_ids:
                following.append(u)

        following_response = UserListSerializer('following', following).get_data()
        followers_response = UserListSerializer('followers', followers).get_data()

        self.data['followers'] = followers_response
        self.data['following'] = following_response
