
from src.models.members.members import Member
from src.models.events.events import Event
from src.common.database import Database

Database.initialize()

events = Event.find_notifications(6)

for event in events:
    print(event.ministry)
    for member in event.assigned_members:
        member = Member.find_by_id(member)
        event.event_email(member.email, member.first_name, member.last_name)
        print(member.first_name + " " + member.last_name + " " + member.email)
