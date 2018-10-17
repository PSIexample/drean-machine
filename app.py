from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.ingredient import Ingredient, IngredientList
from resources.recipe import Recipe, RecipeList


app = Flask(__name__)

### Database data
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'

### App data
app.secret_key = 'psaj'
api = Api(app)

### Creating all database tables before the first run of applications
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

### Adding API endpoints
api.add_resource(RecipeList, '/recipes')
api.add_resource(Recipe, '/recipe/<string:name>')
api.add_resource(IngredientList, '/ingredients')
api.add_resource(Ingredient, '/ingredient/<string:name>')
api.add_resource(UserRegister, '/register')


### Starting an application
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
