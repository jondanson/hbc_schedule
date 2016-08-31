import datetime
from datetime import date, timedelta
import uuid
import requests
from src.common.database import Database
import src.models.events.constants as EventConstants
from src.models.members.members import Member

# todo: still need to make a static method for weekly notification.
# todo: make events repeatable with it's own members list
class Event(object):
    def __init__(self, title, day_of_event, ministry, assigned_members, monthly_notification=False, active=True,
                 _id=None):
        self.title = title
        self.day_of_event = day_of_event
        self.ministry = ministry
        self.assigned_members = assigned_members
        self.monthly_notification = monthly_notification
        self.active = active
        self._id = uuid.uuid4().hex if _id is None else _id

    # todo: add a tag specific note
    def event_email(self, member_email, member_first_name, member_last_name):
        return requests.post(
            EventConstants.URL,
            auth=("api", EventConstants.API_KEY),
            data={
                "from": EventConstants.FROM,
                "to": member_email,
                "subject": "Harvest Baptist Church {}".format(self.ministry),
                "html": "Hello {} {},".format(member_first_name, member_last_name) +
                        "<br><br>You have been scheduled for {} on {} <br>"
                        "during the {}. <br><br>".format(self.ministry, self.day_of_event, self.title) +
                        "<br><br>"
                        "     Thank you,"
                        "<br>       Harvest Baptist Church"
            }
        )

    def save_to_mongo(self):
        Database.update(EventConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "active": self.active,
            "title": self.title,
            "day_of_event": self.day_of_event,
            "ministry": self.ministry,
            "assigned_members": self.assigned_members,
            "_id": self._id
        }

    @classmethod
    def find_notifications(cls, days_before_event):
        time_for_notification = date(int(datetime.date.today().strftime("%Y")),
                                     int(datetime.date.today().strftime("%m")),
                                     int(datetime.date.today().strftime("%d"))) + timedelta(days=days_before_event)
        return [cls(**elem) for elem in Database.find(EventConstants.COLLECTION,
                                                      {"day_of_event": {"$gt": str(time_for_notification)}})]

    @classmethod
    def find_by_title(cls, title):
        return [cls(**elem) for elem in Database.find(EventConstants.COLLECTION,
                                                      {"title": title})]

    @classmethod
    def find_by_id(cls, _id):
        return [cls(**elem) for elem in Database.find(EventConstants.COLLECTION,
                                                      {"_id": _id})]

    @classmethod
    def find_by_ministry(cls, ministry):
        return [cls(**elem) for elem in Database.find(EventConstants.COLLECTION,
                                                      {"ministry": ministry})]

    def inital_monthly_email(self):
        for member in self.assigned_members:
            member = Member.find_by_id(member)
            self.event_email(member.email, member.first_name, member.last_name)

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(EventConstants.COLLECTION, {"active": True})]

    def delete(self):
        Database.remove(EventConstants.COLLECTION, {"_id": self._id})

#Todo: Create cron job for this method
    @staticmethod
    def scan_change_past_events():
        todays_date = date(int(datetime.date.today().strftime("%Y")),
                           int(datetime.date.today().strftime("%m")),
                           int(datetime.date.today().strftime("%d")))
        events = Event.all()
        for event in events:
            if event.day_of_event < todays_date:
                event.active = False
                event.save_to_mongo()
        pass
