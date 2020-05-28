# Name: Time.py
# Description: Time zone manager and utils

# Ver.	Writer			    Date			Notes
# 1.0   Joseph Liu          05/15/20		Original
# 0.2   Kyler Rosen         05/25/20        Changed date assignments for toUTC

from datetime import datetime, timedelta
from pytz import timezone
import pytz


t_starttime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=timezone("America/Los_Angeles").utcoffset(datetime.now()).total_seconds() / 3600)
t_tzs = pytz.all_timezones
r_tzs = dict()
o_tzs = dict()
for i in t_tzs:
    i = str(i)
    r_tzs[i] = timezone(i)

def setStartDate(y, m, d):
    t_starttime = datetime(year=y, month=m, day=d) - timedelta(hours=timezone("America/Los_Angeles").utcoffset(datetime(year=y, month=m, day=d)).total_seconds() / 3600)

def timeSinceStart(t):
    return (t - t_starttime).total_seconds() / 3600
    
def offsetStartTime(time):
    return t_starttime + time

def toUTCOffset(tzName, time):
    return r_tzs[tzName].utcoffset(time).total_seconds() / 3600

def toUTC(tzName, time):
    offset = toUTCOffset(tzName, time)
    return (time + timedelta(hours=offset * -1))

def flightToDatetime(s):
    s = s.split(":")
    return t_starttime.replace(hour=int(s[0]), minute=int(s[1]), second=0, microsecond=0)