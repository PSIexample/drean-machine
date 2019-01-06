from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.order import OrderModel
from models.recipe import RecipeModel
from models.user import UserModel

class NewOrder(Resource):

    @jwt_required()
    def post(self, value):
        user = UserModel.find_by_id(current_identity.id)
        user.current_order = RecipeModel.find_by_value(value).id
        user.save_to_db()
        return {"user": current_identity.id, "current_order": current_identity.current_order}


class OrderHistory(Resource):
    
    @jwt_required()
    def get(self, username):
        user = UserModel.find_by_username(username)
        drink_history = []
        drink_history_query = OrderModel.find_by_user(user.id)
        for row in iter(drink_history_query):
            drink_history.append(row.json())

        return {"user": username, "drink history": drink_history}

