import datetime
from datetime import date, timedelta
import uuid
import requests
from src.common.database import Database
import src.models.events.constants as EventConstants
from src.models.members.members import Member


# todo: make events repeatable with it's own members list
class Event(object):
    def __init__(self, title, day_of_event, tag, assigned_members,  monthly_notification=False, _id=None):
        self.title = title
        self.day_of_event = day_of_event
        self.tag = tag
        self.assigned_members = assigned_members
        self.monthly_notification = monthly_notification
        self._id = uuid.uuid4().hex if _id is None else _id

    # todo: add a tag specific note
    def event_email(self, member_email, member_name):
        return requests.post(
            EventConstants.URL,
            auth=("api", EventConstants.API_KEY),
            data={
                "from": EventConstants.FROM,
                "to": member_email,
                "subject": "Harvest Baptist Church {}".format(self.tag),
                "html": "Hello {},".format(member_name) +
                        "<br><br>You have been scheduled for {} on {} <br>"
                        "during the {}. <br><br>".format(self.tag, self.day_of_event, self.title) +
                        "<br><br>"
                        "     Thank you,"
                        "<br>       Harvest Baptist Church"
            }
        )


    def save_to_mongo(self):
        Database.update(EventConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return{
            "title": self.title,
            "day_of_event": self.day_of_event,
            "tag": self.tag,
            "assigned_members": self.assigned_members,
            "_id": self._id
        }

    # todo: create algorithm for finding events for sending notifications
    @classmethod
    def find_notifications(cls, days_before_event):
        time_for_notification = date(int(datetime.date.today().strftime("%Y")),
                                     int(datetime.date.today().strftime("%m")),
                                     int(datetime.date.today().strftime("%d"))) + timedelta(days=days_before_event)
        print (time_for_notification)
        return [cls(**elem) for elem in Database.find(EventConstants.COLLECTION,
                                                      {"day_of_event":  {"$gt": str(time_for_notification)}})]

    @classmethod
    def find_by_title(cls, title):
        return [cls(**elem) for elem in Database.find(EventConstants.COLLECTION,
                                                      {"title": title})]

    def inital_monthly_email(self):
        for member in self.assigned_members:
            member = Member.find_by_id(member)
            self.event_email(member.email, member.name)


# todo: create a way for admins to create calendar(tag) and specific message for them

