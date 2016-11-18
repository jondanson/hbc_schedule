from src.models.members.members import Member
from src.models.events.events import Event
from src.common.database import Database

Database.initialize()

week_ahead = 6

events = Event.find_notifications(week_ahead)

for event in events:
    print(event.ministry)
    for member in event.assigned_members:
        member = Member.find_by_id(member)
        event.event_email(member.email, member.first_name, member.last_name)