from datetime import datetime, timedelta
from pytz import timezone
import time
import pytz

class TZManager:
    def __init__(self):
        tzs = pytz.all_timezones
        self.tzs = dict()
        for i in tzs:
            i = str(i)
            self.tzs[i] = timezone(i)
            print(self.tzs[i])


    def toUTCOffset(self, tzName, y, m, d):
        return self.tzs[tzName].utcoffset(datetime(year=y, month=m, day=d)).total_seconds() / 3600
    
    def toUTC(self, tzName, time):
        offset = self.toUTCOffset(tzName, time.year, time.month, time.day)
        return time + timedelta(hours=offset * -1)

#t = TZManager()
#print(t.toUTC("US/Pacific", datetime.now()))