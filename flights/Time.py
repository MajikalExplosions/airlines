# Name: Time.py
# Description: Time zone manager and utils

# Ver.	Writer			    Date			Notes
# 1.0   Joseph Liu          05/15/20		Original
# 0.2   Kyler Rosen         05/25/20        Changed date assignments for toUTC

from datetime import datetime, timedelta
from pytz import timezone
import time
import pytz


t_starttime = datetime.now().replace(second=0, microsecond=0) - timedelta(hours=timezone("America/Los_Angeles").utcoffset(datetime.now()).total_seconds() / 3600)
t_tzs = pytz.all_timezones
r_tzs = dict()
o_tzs = dict()
for i in t_tzs:
    i = str(i)
    r_tzs[i] = timezone(i)
    o_tzs[i] = r_tzs[i].utcoffset(t_starttime).total_seconds() / 3600

def timeSinceStart(t):
    return (t - t_starttime).total_seconds() / 3600

def offsetStartTime(time):
    return t_starttime + time

def toUTCOffset(tzName, y, m, d):
    return o_tzs[tzName]

def toUTC(tzName, time):
    offset = toUTCOffset(tzName, time.year, time.month, time.day)
    return (time + timedelta(hours=offset * -1)).dateReplace(day = t_starttime.day)

def flightToDatetime(s):
    s = s.split(":")
    return t_starttime.replace(hour=int(s[0]), minute=int(s[1]), second=0, microsecond=0)

#Example code below.  Prints current time in UTC.
#t = TZManager()
#print(t.toUTC("US/Pacific", datetime.now()))