from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.recipe import RecipeModel
from models.mixing import MixingModel

class Recipe(Resource):
# TODO
# GET
# getting ingredients from mixings table
# POST/PUT
# list of available ingredients
# saving mixings to db
# DELETE
# cascade delete from mixing table

    recipe_parser = reqparse.RequestParser()
    mixing_parser = reqparse.RequestParser()
    recipe_parser.add_argument('voltage',
        type=int
    )
    recipe_parser.add_argument('ingredients_list',
        type=dict,
        required=True,
        action='append',
        help="Add ingredients",
        location="json"
    )

    def get(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404

    def post(self, name):
        recipe_data = Recipe.recipe_parser.parse_args()
        portion_sum = 0
        if RecipeModel.find_by_name(name):
            return {'message': "Recipe '{}' already exist".format(name)}, 400

        recipe = RecipeModel(name)
        for mixing in iter(recipe_data['ingredients_list']):
            portion_sum = portion_sum + mixing['portion']
        if portion_sum > 200:
            return {"meessage": "portion over limit"}
        
        try:
            recipe_id = recipe.save_to_db()
            for mixing in iter(recipe_data['ingredients_list']):
                mixing_model = MixingModel(mixing['ingredient_id'], recipe_id, mixing['portion'])
                mixing_model.save_to_db()
                print(mixing['ingredient_id'])
        except:
            return {'message': 'An error occured'}, 500

        return portion_sum, 201

   # def put(self, name):
                
        data = Recipe.parser.parse_args()
        recipe = RecipeModel.find_by_name(name)

        if recipe:
            recipe.ingredients_list = data['ingredients_list']
        else:
            recipe = RecipeModel(name, **data)
        
        try:
            recipe.save_to_db()
        except:
            return {'message': 'An error occured'}, 500

        return recipe.json()

    def delete (self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            recipe.delete_from_db()
            return {'message': 'Recipe deleted'}
        return {'message': 'No such recipe'}


class RecipeList(Resource):
    def get(self):
        return {'recipes': list(map(lambda x: x.json(), RecipeModel.query.all()))}