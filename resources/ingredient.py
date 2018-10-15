from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.ingredient import IngredientModel
from models.mixing import MixingModel

class Ingredient(Resource):

# TODO
# add voltage
# change amount after each request    

    parser = reqparse.RequestParser()
    parser.add_argument('amount',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    def get(self,name):
        ingredient = IngredientModel.find_by_name(name)
        if ingredient:
            possible_drinks = MixingModel.find_by_ingredient(ingredient.id)
            return {"ingredient": ingredient.json()}
        return {"message": 'Ingredient not found'}, 404

    @jwt_required()
    def post(self, name):
        if IngredientModel.find_by_name(name):
            return {'message': "Item '{}' already exists".format(name)}, 400
         
        data = Ingredient.parser.parse_args()
        item = IngredientModel(name, **data)
        
        item = IngredientModel(name, **data)
        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def put(self, name):
        
        data = Ingredient.parser.parse_args()
        ingredient = IngredientModel.find_by_name(name)

        if ingredient:
            ingredient.amount = data['amount']
        else:
            ingredient = IngredientModel(name, **data)

        ingredient.save_to_db()
        return ingredient.json()

    @jwt_required
    def delete(self, name):
        ingredient = IngredientModel.find_by_name(name)
        if ingredient:
            ingredient.delete_ingredient()
            return {"message": "Item deleted"}
        return {"message": "No such item"}

class IngredientList(Resource):
    def get(self):
        return {'ingredients': list(map(lambda x: x.json(), IngredientModel.query.all()))}
