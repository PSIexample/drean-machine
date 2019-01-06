from flask_restful import Resource, reqparse
from datetime import datetime

from models.recipe import RecipeModel
from models.user import UserModel, UserCardRegistrationModel
from models.order import OrderModel

from resources.recipe import Recipe
from resources.user import UserCardRegistration


#This request goes directly to Drean Machine
class LetsDrink(Resource):

    def get(self, rfid):
        user = UserModel.find_by_rfid(rfid)
        if user:
            current_order = int(user.current_order)
            recipe = RecipeModel.find_by_id(current_order)
            ingredients = RecipeModel.find_ingredients(current_order)
            durations = [0, 0, 0, 0]

            for ingredient in ingredients:
                durations[ingredient[0]['pump']-1] = ingredient[0]['portion']

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            order = OrderModel(user.id,user.current_order,timestamp)
            order.save_to_db()
            return {"durations": durations}

        awaiting = UserCardRegistrationModel.awaiting_for_card

        if awaiting:
            if UserModel.find_by_username(awaiting):
                UserModel.update_card(awaiting, rfid)
                return {"durations": [0, 0, 0, 0]}
            else:
                return {"message": "No such user"}
        else:
            return {"durations": [0, 0, 0, 0]}