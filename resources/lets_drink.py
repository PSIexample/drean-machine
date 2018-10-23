from flask_restful import Resource, reqparse
from datetime import datetime

from models.recipe import RecipeModel
from models.user import UserModel
from models.order import OrderModel
    
class LetsDrink(Resource):

    def post(self, rfid):
        user = UserModel.find_by_rfid(rfid)
        if user:
            recipe = RecipeModel.find_by_id(user.current_order)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            order = OrderModel(user.id,user.current_order,timestamp)
            order.save_to_db()
            return {"message": "Your order has been realised", "user": user.username, "recipe": recipe.name}

        else:
            ##Redirect to rfid registration
            return {"message": "Chip not assigned to any user"}