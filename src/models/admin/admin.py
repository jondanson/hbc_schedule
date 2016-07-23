import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.admin.errors as AdminErrors
import src.models.admin.constants as AdminConstants


class Admin(object):
    def __init__(self, email, password, active=True, _id=None):
        self.email = email
        self.password = password
        self.active = active
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def is_login_valid(email, password):
        user_data = Database.find_one(AdminConstants.COLLECTION, {"email": email})

        if user_data is None:
            raise AdminErrors.AdminNotExistError("Your email or password is wrong. <br>"
                                                 "Contact your admin if you need help"
                                                 "accessing your account.")
            pass
        if not Utils.check_hashed_password(password, user_data['password']):
            raise AdminErrors.AdminPasswordNotCorrect("Your email or password is wrong. "
                                                      "Contact your admin if you need help"
                                                      "accessing your account.")
            pass

        return True

    @staticmethod
    def register_admin(email, password):
        user_data = Database.find_one(AdminConstants.COLLECTION, {"email": email})

        if user_data is not None:
            raise AdminErrors.AdminAlreadyRegisteredError("The email you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise AdminErrors.InvalidEmailError("Not a valid email format.")

        Admin(email, Utils.hash_password(password)).save_to_mongo()

    def save_to_mongo(self):
        Database.update(AdminConstants.COLLECTION, {"_id": self._id}, self.json())


    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    def delete(self):
        Database.remove(AdminConstants.COLLECTION, {"_id": self._id})


    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(AdminConstants.COLLECTION, {'email': email}))
