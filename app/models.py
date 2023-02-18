from flask_login import UserMixin
from .db_services import get_user

class UserData:
    def __init__(self, user_name, user_password):
        self.name = user_name
        self.password = user_password

class UserModel(UserMixin):
    def __init__(self, user_data: UserData):
        self.id = user_data.name
        self.password = user_data.password

    @staticmethod
    def query(user_id):
        user_dict = get_user(user_id)
        user_data = UserData(
                user_id,
                user_dict["usr-passwrd"]
                )
        return UserModel(user_data)
