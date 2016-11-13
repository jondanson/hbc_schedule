import uuid
import requests
import src.config as DEBUG
from src.common.database import Database
from src.common.utils import Utils
import src.models.groups.gconstants as GroupConstants
import src.models.groups.errors as GroupErrors


class Groups(object):
    def __init__(self, group_name, assigned_members, _id=None):
        self.group_name = group_name
        self.assigned_members = assigned_members
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def register_group(group_name, assigned_members):

        Groups(group_name, assigned_members).save_to_mongo()

        return True

    def save_to_mongo(self):
        Database.update(GroupConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "group_name": self.group_name,
            "assigned_members": self.assigned_members,
        }

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(GroupConstants.COLLECTION, {})]

    @classmethod
    def find_by_id(cls, _id):
        return cls(**Database.find_one(GroupConstants.COLLECTION, {'_id': _id}))