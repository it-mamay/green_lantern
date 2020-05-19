from itertools import count
from store_app import NoSuchUserError


class FakeStorage:
    def __init__(self):
        self._users = FakeUsers()
        self._goods = FakeGoods()
        # self._stores = FakeStores()

    @property
    def users(self):
        return self._users

    @property
    def goods(self):
        return self._goods

    # @property
    # def stores(self):
    #     return self._stores

class FakeUsers:
    def __init__(self):
        self._users = {}
        self._id_counter = count(1)

    def add(self, user):
        user_id = next(self._id_counter)
        self._users[user_id] = user
        return user_id

    def get_user_by_id(self, user_id):
        try:
            return self._users[user_id]
        except KeyError:
            raise NoSuchUserError(user_id)

    def update_user_by_id(self, user_id, user):
        if user_id in self._users:
            self._users[user_id] = user
        else:
            raise NoSuchUserError(user_id)

class FakeGoods:

    def __init__(self):
        self._goods = {}
        self._id_counter = count(1)

    def add(self, goods):
        for item in goods:
            self._goods[next(self._id_counter)] = item
        return len(goods)

    def get_goods(self):
        response = []
        for goods in self._goods.items():
            tmp = goods[1]
            _id = {'id': goods[0]}
            tmp.update(_id)
            response.append(tmp)
        return response

#     def update_goods(self, goods_upd):
#         updated = 0
#         not_exist = []
#         for good in goods_upd:
#             id_upd = good['id']
#             data_upd = self._goods.get(id_upd, '')
#             # found id for update
#             if data_upd:
#                 self._goods.update({id_upd: good})
#                 updated += 1
#             else:
#                 not_exist.append(id_upd)
#
#         return {'successfully_updated': updated, 'errors': {'no such id in goods': not_exist}}
#
# class FakeStores:
#
#     def __init__(self):
#         self._stores = {}
#         self._id_counter = count(1)
