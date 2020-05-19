# Name: Time.py
# Description: Time zone manager and utils

# Ver.	Writer			    Date			Notes
# 1.0   Joseph Liu          05/15/20		Original

from datetime import datetime, timedelta
from pytz import timezone
import time
import pytz

t_tzs = pytz.all_timezones
r_tzs = dict()
for i in t_tzs:
    i = str(i)
    r_tzs[i] = timezone(i)


def toUTCOffset(tzName, y, m, d):
    return r_tzs[tzName].utcoffset(datetime(year=y, month=m, day=d)).total_seconds() / 3600

def toUTC(tzName, time):
    offset = toUTCOffset(tzName, time.year, time.month, time.day)
    return time + timedelta(hours=offset * -1)

def flightToDatetime(s):
    s = s.split(":")
    return datetime.now().replace(hour=int(s[0]), minute=int(s[1]), second=0, microsecond=0)

#Example code below.  Prints current time in UTC.
#t = TZManager()
#print(t.toUTC("US/Pacific", datetime.now()))