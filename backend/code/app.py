from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS, cross_origin

from security import authenticate, identity
from resources.user import UserRegister, UserCardRegistration
from resources.ingredient import Ingredient, IngredientList, Test, PumpList
from resources.recipe import Recipe, NewRecipe, RecipeList
from resources.order import NewOrder, OrderHistory
from resources.lets_drink import LetsDrink

app = Flask(__name__, static_url_path='/front/')
CORS(app)

### Database data
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'

### App data
app.secret_key = 'bartender'
api = Api(app)

### Creating all database tables before the first run of applications
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

@app.route('/index')
def root():
    return app.send_static_file('index.html')

### Adding API endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(UserCardRegistration, '/card-register/<string:username>')
api.add_resource(RecipeList, '/recipes')
api.add_resource(Recipe, '/recipe/<string:value>')
api.add_resource(NewRecipe, '/recipe/new')
api.add_resource(IngredientList, '/ingredients')
api.add_resource(Ingredient, '/ingredient/<string:value>')
api.add_resource(NewOrder, '/recipe/<string:value>/new-order')
api.add_resource(OrderHistory, '/user/<string:username>/realised')
api.add_resource(PumpList, '/pumps')
api.add_resource(LetsDrink, '/lets-drink/<string:rfid>')

api.add_resource(Test, '/test')


### Starting an application
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, host='0.0.0.0', threaded=True, debug=True)
