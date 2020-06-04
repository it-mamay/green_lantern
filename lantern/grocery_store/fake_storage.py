from itertools import count
from store_app import NoSuchUserError, NoSuchUserID, NoSuchStoreID, NoSuchManagerID


class FakeStorage:
    def __init__(self):
        self._users = FakeUsers()
        self._goods = FakeGoods()
        self._stores = FakeStores()

    @property
    def users(self):
        return self._users

    @property
    def goods(self):
        return self._goods

    @property
    def stores(self):
        return self._stores


class FakeUsers:
    def __init__(self):
        self._users = {}
        self._id_counter = count(1)
        self._goods = {}
        self._stores = {}

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


class FakeGoods(FakeUsers):

    def add_goods(self, goods):
        for good in goods:
            goods_id = next(self._id_counter)
            self._goods[goods_id] = good
        return len(goods)

    def get_full_info_of_goods(self):
        full_info = []
        for key, value in self._goods.items():
            full_info.append({**value, 'id': key})
        return full_info

    def put_info_on_goods(self, goods):
        success_good = 0
        error_goods_id = []

        for new_value in goods:
            if new_value['id'] in self._goods.keys():
                self._goods[new_value['id']] = new_value
                success_good += 1
            else:
                error_goods_id.append(new_value['id'])
        return success_good, error_goods_id


class FakeStores(FakeUsers):

    def create_new_store(self, store):
        try:
            store_id = next(self._id_counter)
            self._stores[store_id] = store
            return store_id
        except KeyError:
            raise NoSuchUserID(store_id)

    def get_full_info(self, store_id):
        try:
            full_stores = self._stores[store_id]
            return full_stores
        except KeyError:
            raise NoSuchStoreID(store_id)

    def update_store(self, store, store_id):
        if store_id not in self._stores.keys():
            raise NoSuchStoreID(store_id)
        self._stores[store_id] = {**self._stores[store_id], **store}
        return self._stores[store_id]
