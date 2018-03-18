from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


items = []

class Item(Resource):
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

class ReturnAllItems(Resource):
    def get(self):
        return {'Items': items}, 200

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ReturnAllItems, '/items')

app.run(port = 4000, debug=True)
