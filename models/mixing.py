import sqlite3
from db import db

class MixingModel(db.Model):
    __tablename__ = 'mixings'

    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE')) #lazy = 'dynamic'
    portion = db.Column(db.Integer)

    ingredient = db.relationship('IngredientModel')
    recipe = db.relationship('RecipeModel')

    def __init__(self,ingredient_id,recipe_id,portion):
        self.ingredient_id = ingredient_id
        self.recipe_id = recipe_id
        self.portion = portion

    def json(self):
        return {'portion': self.portion}

    @classmethod
    def find_by_ingredient(cls, ingredient_id):
        return cls.query.filter_by(ingredient_id=ingredient_id).all()

    @classmethod
    def find_by_recipe(cls, recipe_id):
        return cls.query.filter_by(recipe_id=recipe_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()