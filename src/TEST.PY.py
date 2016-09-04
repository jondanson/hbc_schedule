import time
import datetime
from datetime import date, timedelta
from src.models.members.members import Member
from src.models.events.events import Event
from src.common.database import Database

Database.initialize()

# mem = Member.all()

# print (type (mem))

# for members in mem:
#    print (members._id)

# event = Event("Sunday Evening Service", "2016-9-15", "Security", [mem[0]._id, mem[1]._id, mem[2]._id, mem[3]._id, mem[4]._id])



# event.save_to_mongo()

events = Event.all()
event1 = []
for event in events:
    this = Event.find_by_id(event._id)

    for it in this:
        print(it.title)


