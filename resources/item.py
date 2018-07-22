from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=False,
        help="This field cannot be left blank!"
    )
    parser.add_argument('sitename',
        type=str,
        required=True,
        help="Every item needs a sitename."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        data = Item.parser.parse_args()
        if ItemModel.find_by_itemname_sitename(name,data['sitename']):
            return {'message': "An item with name '{}' already exists on site.".format(name)}, 400

        #data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['sitename'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the {} item.".format(name)}, 500

        return item.json(), 201

    def delete(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_itemname_sitename(name,data['sitename'])
        if item :
            item.delete_from_db()

        return {'message': "Item {} deleted".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()

        #item = ItemModel.find_by_name(name)
        item = ItemModel.find_by_itemname_sitename(name,data['sitename'])

        #if ItemModel.find_by_store_itemname_storename(name,data['store_name']):
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'],data['sitename'])

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'ItemList': list(map(lambda x: x.json(), ItemModel.query.all()))}
