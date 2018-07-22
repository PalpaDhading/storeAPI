from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('street',
            type =str,
            required = True,
            help ="This field can't be left blank "
        )
    parser.add_argument('city',
            type =str,
            required = True,
            help ="This field can't be left blank "
        )
    parser.add_argument('state',
            type =str,
            required = True,
            help ="This field can't be left blank "
        )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        data = Store.parser.parse_args()
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name,data['street'],data['city'],data['state'])
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def put(self, name):
        data = Store.parser.parse_args()

        store =  StoreModel.find_by_name(name)

        if store:
            store.street = data['street']
            store.city = data['city']
            store.state = data['state']

        else:
            store = StoreModel(name,data['street'],data['city'],data['state'])

        store.save_to_db()

        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'Stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
