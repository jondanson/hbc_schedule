import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.members.constants as MemberConstants
import src.models.members.errors as MemberErrors


class Member(object):
    def __init__(self, name, email="na", cell_phone="na", active="True", _id=None):
        self.name = name
        self.email = email
        self.cell_phone = cell_phone
        self.active = active
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def register_member(name, email, cell_phone):
        """
        Registers a Member. The Admin will have to create
        himself as a general user for scheduling purposes.
        :param name: user's name
        :return: True if registered successfully or False if otherwise (exceptions can be raised)
        """
        if not Utils.email_is_valid(email):
            raise MemberErrors.InvalidEmailError("Not a valid email format.")

        Member(name, email, cell_phone).save_to_mongo()

        return True

    def save_to_mongo(self):
        Database.update(MemberConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "cell_phone": self.cell_phone,
            "active": self.active
        }

    # todo: Figure out running each member and creating a list of services and dates to send the entire schedule for a month
    # todo: Write out message for the full schedule.
    def monthly_email(self, member_email, member_name):
        return requests.post(
            MemberConstants.URL,
            auth=("api", MemberConstants.API_KEY),
            data={
                "from": MemberConstants.FROM,
                "to": member_email,
                "subject": "Harvest Baptist Church {}".format(self.tag),
                "html": "Hello {}, <br><br>You have been scheduled for {} on {} <br>"
                        "during the {}. <br><br> Thank you,"
                        "<br> Harvest Baptist Church".format(member_name, self.tag, self.date, self.title)
            }
        )

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(MemberConstants.COLLECTION, {'email': email}))

    @classmethod
    def find_by_name(cls, name):
        return cls(**Database.find_one(MemberConstants.COLLECTION, {'name': name}))

    @classmethod
    def find_by_id(cls, _id):
        return cls(**Database.find_one(MemberConstants.COLLECTION, {'_id': _id}))

    @classmethod
    def all_members(cls):
        return [cls(**elem) for elem in Database.find(MemberConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(MemberConstants.COLLECTION, {"_id": self._id})
