from flask import Flask, jsonify, request

import inject


class NoSuchUserError(Exception):
    def __init__(self, user_id):
        self.message = f'No such user_id {user_id}'


class NoSuchUserID(Exception):
    def __init__(self, store_id):
        self.message = f'No such user id: {store_id}'


class NoSuchStoreID(Exception):
    def __init__(self, store_id):
        self.message = f'No such store id: {store_id}'


class NoSuchManagerID(Exception):
    def __init__(self, manager_id):
        self.message = f'No such store id: {manager_id}'


app = Flask(__name__)


@app.errorhandler(NoSuchUserError)
def my_error_handler(e):
    return jsonify({'error': e.message}), 404


@app.errorhandler(NoSuchUserID)
def error_for_not_found_id(e):
    return jsonify({'Error': e.message}), 404


@app.errorhandler(NoSuchStoreID)
def error_for_not_found_store_id(e):
    return jsonify({'Error': e.message}), 404


@app.errorhandler(NoSuchManagerID)
def error_for_not_found_manager_id(e):
    return jsonify({'Error': e.message}), 404


@app.route('/users', methods=['POST'])
def create_user():
    db = inject.instance('DB')
    user_id = db.users.add(request.json)
    return jsonify({'user_id': user_id}), 201


@app.route('/users/<int:user_id>')
def get_user(user_id):
    db = inject.instance('DB')
    user = db.users.get_user_by_id(user_id)
    return jsonify(user)


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    db = inject.instance('DB')
    db.users.update_user_by_id(user_id, request.json)
    return jsonify({'status': 'success'})


@app.route('/goods', methods=['POST'])
def create_goods():
    db = inject.instance('DB')
    goods = db.goods.add_goods(request.json)
    return jsonify({'numbers of items created': len(request.json)}), 201


@app.route('/goods')
def get_goods():
    db = inject.instance('DB')
    goods = db.goods.get_full_info_of_goods()
    return jsonify(goods), 200


@app.route('/goods', methods=['PUT'])
def update_goods():
    db = inject.instance('DB')
    succes_count, error_ids = db.goods.put_info_on_goods(request.json)
    return jsonify(
        {
            'successfully_updated': succes_count,
            'errors': {'no such id in goods': error_ids}
        }
    ), 200


@app.route('/store', methods=['POST'])
def create_store():
    db = inject.instance('DB')
    store_id = db.stores.create_new_store(request.json)
    return jsonify({'stored_id': store_id}), 201


@app.route('/store/<int:store_id>')
def get_stores(store_id):
    db = inject.instance('DB')
    full_stores_info = db.stores.get_full_info(store_id)
    return jsonify(full_stores_info), 200


@app.route('/store/<int:store_id>', methods=['PUT'])
def update_store(store_id):
    db = inject.instance('DB')
    result = db.stores.update_store(request.json, store_id)
    return jsonify(result), 200
