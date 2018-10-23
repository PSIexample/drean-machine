from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.ingredient import IngredientModel
from models.recipe import RecipeModel
from models.mixing import MixingModel

class Ingredient(Resource):

# TODO
# change amount after each request    


### Define values for ingredient parser
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('amount',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('voltage',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('pump',
        type=int,
    )

### getting list of possible drinks with ingredient with name requested in URL
    def get(self,value):
        def find_possible_drinks(ingredient_id):
            possible_drinks_dict = []
            possible_drinks = MixingModel.find_by_ingredient(ingredient_id)
            for row in iter(possible_drinks):
                drink = RecipeModel.find_by_id(row.recipe_id)
                possible_drinks_dict.append(drink.json())
            return possible_drinks_dict

        ingredient = IngredientModel.find_by_value(value)
        if ingredient:
            possible_drinks_dict = find_possible_drinks(ingredient.id)
            return {"ingredient": ingredient.json(), "possible drinks": possible_drinks_dict}
        return {"message": 'Ingredient not found'}, 404

    @jwt_required()
    def post(self, value):
        if IngredientModel.find_by_value(value):
            return {'message': "Item '{}' already exists".format(value)}, 400
         
        data = Ingredient.parser.parse_args()
        item = IngredientModel(value, **data)
        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def put(self, value):
        print(current_identity.username)
        data = Ingredient.parser.parse_args()
        ingredient = IngredientModel.find_by_value(value)

        if ingredient:
            ingredient.name = data['name']
            ingredient.amount = data['amount']
            ingredient.voltage = data['voltage']
            ingredient.pump = data['pump']
        else:
            ingredient = IngredientModel(value, **data)

        ingredient.save_to_db()
        return ingredient.json()

    @jwt_required()
    def delete(self, value):
        ingredient = IngredientModel.find_by_value(value)
        if ingredient:
            ingredient.delete_from_db()
            return {"message": "Item deleted"}
        return {"message": "No such item"}

class IngredientList(Resource):
    def get(self):
        return {'ingredients': list(map(lambda x: x.json(), IngredientModel.query.all()))}
