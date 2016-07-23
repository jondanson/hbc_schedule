import time
import datetime
from datetime import date, timedelta
from src.models.members.members import Member
from src.models.events.events import Event
from src.common.database import Database

Database.initialize()

#mem=[]

#mem = Member.all_members()

#print (type (mem))

#for members in mem:
#    print (members._id)

#event = Event("Sunday Morning Service", "2016-7-15", "Security",
              #[mem[0]._id, mem[1]._id, mem[2]._id, mem[3]._id, mem[4]._id])



#event.save_to_mongo()

events = Event.find_notifications(7)

for event in events:
    event.week_before_reminder()
    print(event.tag, event.title)