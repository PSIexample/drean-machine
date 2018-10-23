from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help="This field cannot be blank"
    )

    parser.add_argument('password',
    type=str,
    required=True,
    help="This field cannot be blank"
    )

    parser.add_argument('current_order',
    type=int,
    required=False
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "Username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201

    @jwt_required()
    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {"message": "User deleted"}, 201
        return {"message": "No such item"}