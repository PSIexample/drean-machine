from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


from models.recipe import RecipeModel
from models.mixing import MixingModel
from models.ingredient import IngredientModel

from resources.ingredient import IngredientList

class Recipe(Resource):
# TODO
# GET
# getting ingredients from mixings table
# POST/PUT
# list of available ingredients
# DELETE
# cascade delete from mixing table

### Parser section
    recipe_parser = reqparse.RequestParser()
    #mixing_parser = reqparse.RequestParser()
    recipe_parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    recipe_parser.add_argument('ingredients_list',
        type=dict,
        required=True,
        action='append',
        help="Add ingredients",
        location="json"
    )

### Returns the recipe for a cocktail. Gets parameter from request URL
    def get(self, value):
        recipe = RecipeModel.find_by_value(value)
        
        if recipe:
            ingredients = RecipeModel.find_ingredients(recipe.id)
            return {"recipe": recipe.json(), "ingredients": ingredients}

        return {'message': 'Recipe not found'}, 404

    @jwt_required()
    def post(self, value):
        recipe_data = Recipe.recipe_parser.parse_args()
        portion_sum = 0

        if RecipeModel.find_by_value(value):
            return {'message': "Recipe '{}' already exist".format(value)}, 400

        recipe = RecipeModel(value, recipe_data['name'])
        for mixing in iter(recipe_data['ingredients_list']):
            portion_sum = portion_sum + mixing['portion']
        if portion_sum > 200:
            return {"meessage": "portion over limit"}
        
        try:
            recipe_id = recipe.save_to_db()
            for mixing in iter(recipe_data['ingredients_list']):
                mixing_model = MixingModel(mixing['ingredient_id'], recipe_id, mixing['portion'])
                mixing_model.save_to_db()
        except:
            return {'message': 'An error occured during saving to DB'}, 500
        
        return recipe.json(), 201

    @jwt_required()
    def delete (self, value):
        recipe = RecipeModel.find_by_value(value)
        if recipe:
            mixings_to_delete = MixingModel.find_by_recipe(recipe.id)
            for row in iter(mixings_to_delete):
                row.delete_from_db()
            recipe.delete_from_db()
            return {'message': 'Recipe deleted'}
        return {'message': 'No such recipe'}

class NewRecipe(Resource):
    def get(self):
        possible_ingredients = IngredientList.get(self)
        return possible_ingredients

class RecipeList(Resource):
    def get(self):
        return {'recipes': list(map(lambda x: x.json(), RecipeModel.query.all()))}