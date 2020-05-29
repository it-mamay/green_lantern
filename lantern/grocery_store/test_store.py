import inject

from store_app import app
from fake_storage import FakeStorage


def configure_test(binder):
    db = FakeStorage()
    binder.bind('DB', db)


class Initializer:
    def setup(self):
        inject.clear_and_configure(configure_test)

        app.config['TESTING'] = True
        with app.test_client() as client:
            self.client = client


class TestUsers(Initializer):

    def test_create_new(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        assert resp.status_code == 201
        assert resp.json == {'user_id': 1}

        resp = self.client.post(
            '/users',
            json={'name': 'Ihor Melnyk'}
        )
        assert resp.json == {'user_id': 2}

    def test_successful_get_user(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        user_id = resp.json['user_id']
        resp = self.client.get(f'/users/{user_id}')
        assert resp.status_code == 200
        assert resp.json == {'name': 'John Doe'}

    def test_get_unexistent_user(self):
        resp = self.client.get('/users/1')
        assert resp.status_code == 404
        assert resp.json == {'error': 'No such user_id 1'}

    def test_successful_update_user(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        user_id = resp.json['user_id']
        resp = self.client.put(
            f'/users/{user_id}',
            json={'name': 'Johanna Doe'}
        )
        assert resp.status_code == 200
        assert resp.json == {'status': 'success'}

    def test_unexistent_update_user(self):
        resp = self.client.put(
            '/users/1',
            json={'name': 'Johanna Doe'}
        )
        assert resp.status_code == 404
        assert resp.json == {'error': 'No such user_id 1'}


class TestGoods(Initializer):

    def test_create_goods(self):
        resp = self.client.post(
            '/goods',
            json=[
                {'name': 'Chocolate_bar', 'price': 10},
                {'name': 'Vodka', 'price': 150}
            ]
        )
        assert resp.status_code == 201
        assert resp.json == {'numbers of items created': 2}  # len(resp.json)

    def test_successful_get_goods(self):
        resp = self.client.post(
            '/goods',
            json=[
                {'name': 'Chocolate_bar', 'price': 10},
                {'name': 'Vodka', 'price': 150},
                {'name': 'Viskaryk', 'price': 500},
                {'name': 'Shmurdyak_try_topora', 'price': 15}
            ]
        )
        resp = self.client.get('/goods')
        assert resp.status_code == 200
        assert resp.json == [
            {'name': 'Chocolate_bar', 'price': 10, 'id': 1},
            {'name': 'Vodka', 'price': 150, 'id': 2},
            {'name': 'Viskaryk', 'price': 500, 'id': 3},
            {'name': 'Shmurdyak_try_topora', 'price': 15, 'id': 4}
        ]

    def test_successful_update_goods(self):
        resp = self.client.post(
            '/goods',
            json=[
                {'name': 'Chocolate_bar', 'price': 10, 'id': 1},
                {'name': 'Vodka', 'price': 150, 'id': 2},
                {'name': 'Viskaryk', 'price': 500, 'id': 3},
                {'name': 'Shmurdyak_try_topora', 'price': 15, 'id': 4}
            ]
        )

        resp = self.client.put(
            '/goods',
            json=[
                {'name': 'Chocolate_bar', 'price': 11, 'id': 1},
                {'name': 'Vodka', 'price': 151, 'id': 2},
                {'name': 'Viskaryk', 'price': 500, 'id': 3},
                {'name': 'Shmurdyak_try_topora', 'price': 15, 'id': 4},
                {'name': 'Shmurdyak_try_topora', 'price': 15, 'id': 5}
            ]
        )
        assert resp.status_code == 200
        assert resp.json == {
            'successfully_updated': 4,
            'errors': {'no such id in goods': [5]}
        }
