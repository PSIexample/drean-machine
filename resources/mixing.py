import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.ingredient import IngredientModel


class Mixing(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('store_id',
        type=float,
        required=True,
        help="Every item needs store"
    )