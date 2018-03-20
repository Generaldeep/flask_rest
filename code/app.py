from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'thisisasecretykey'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'item': 'item with name {} already exists'.format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items ))
        return {'message': 'item has been deleted'}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type = float,
            required = True,
            help = 'This field cannot be left blank'
        )

        data = parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ReturnAllItems(Resource):
    def get(self):
        return {'Items': items}, 200

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ReturnAllItems, '/items')

app.run(port = 4000, debug=True)
