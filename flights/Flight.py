# Name: Flight.py
# Description: Stores data for a single flight

# Ver.	Writer			    Date			Notes
# 0.1   Kyler Rosen         05/09/20		Add flight info from file except days
# 0.2   Joseph Liu			05/15/20		Renaming, add parsing for days, add travel time
# 0.3   Kyler Rosen         05/20/20        Fixed consideration for days, timezones, etc

from flights.Time import *
from datetime import timedelta

class Flight:
    def __init__(self, i, airline, num, origin, destination, depTime, arrTime, days):
        #Python has built-in ids, so we can't use the self.id property
        self.flightId = i
        self.airline = airline
        self.number = num
        self.origin = origin
        self.destination = destination
        self.departureTime = depTime
        self.arrivalTime = arrTime
        arrivalTimeAdd = False
        arrivalTimeSubtract = False
        arrivalTimeAdd2 = False

        if self.arrivalTime.find("-") != -1 or self.arrivalTime.find("+") != -1:
            if self.arrivalTime.find("-") != -1:
                arrivalTimeSubtract = True

            if self.arrivalTime.find("+1") != -1:
                arrivalTimeAdd = True

            if self.arrivalTime.find("+2") != -1:
                arrivalTimeAdd2 = True


            self.arrivalTime = self.arrivalTime[:-2]

        self.arrivalTimeLocal = flightToDatetime(self.arrivalTime)
        self.arrivalTime = toUTC(self.destination.getTimezone(), flightToDatetime(self.arrivalTime))
        if arrivalTimeAdd:
            self.arrivalTime += timedelta(hours = 24)

        elif arrivalTimeAdd:
            self.arrivalTime += timedelta(hours = 48)

        elif arrivalTimeSubtract:
            self.arrivalTime -= timedelta(hours = 24)

        self.departureTimeLocal = flightToDatetime(self.departureTime)
        self.departureTime = toUTC(self.origin.getTimezone(), flightToDatetime(self.departureTime))

        #Add days where flight is run
        if days == "Daily":
            self.runsOn = [True, True, True, True, True, True, True]
        else:
            #Not daily flight
            if days[0] == "X":
                self.runsOn = [True, True, True, True, True, True, True]
                days = days[1:]
            else:
                self.runsOn = [False, False, False, False, False, False, False]
            
            #For each
            for i in range(len(days)):
                self.runsOn[int(days[i]) - 1] = not self.runsOn[int(days[i]) - 1]

    def getID(self):
    	return self.flightId

    def getAirline(self):
    	return self.airline
        
    def getNumber(self):
        return self.number

    def getOrigin(self):
        return self.origin

    def getDestination(self):
        return self.destination

    def getDepTime(self):
        return self.departureTime

    def getArrTimeLocal(self):
        return self.arrivalTimeLocal

    def getDepTimeLocal(self):
        return self.departureTimeLocal

    def getArrTime(self):
        return self.arrivalTime
    
    def getTravelTime(self):
        td = self.arrivalTime - self.departureTime
        #td.total_seconds / 3600
        return (td.total_seconds() / 3600)

    #Note: this function needs optimizing.
    def timeUntilNextFlight(self, time):
        #First convert to local time
        time += timedelta(hours=toUTCOffset(self.getOrigin().getTimezone(), time.year, time.month, time.day))

        #Find next day that flight runs
        if time.hour * 60 + time.minute > self.getDepTimeLocal().hour * 60 + self.getDepTimeLocal().minute:
            time = time + timedelta(days=1)
            offset = True
        else:
            offset = False

        day = time.weekday()
        if offset:
            initialDay = day - 1
        else:
            initialDay = day

        while not self.runsOn[day]:
            day = (day + 1)
            if day >= 7:
                day = day % 7
                initialDay -= 7
        
        #Old:
        #runDay = time.replace(hour=0, minute=0) + timedelta(days=day - initialDay)
        #negativeOffset = time.replace(hour=0, minute=0) - time
        #startTime = runDay + timedelta(hours=time.hour, minutes=time.minute) + negativeOffset + timedelta(hours=self.getDepTimeLocal().hour, minutes=self.getDepTimeLocal().minute)
        #return (startTime - time).totalSeconds() / 3600

        return timedelta(days=day - initialDay, hours=self.getDepTimeLocal().hour - time.hour, minutes=self.getDepTimeLocal().minute - time.minute).total_seconds() / 3600
    
    def toString(self):
        return "Flight " + self.airline + str(self.number) + " from " + self.origin.toString() + " to " + self.destination.toString() + " (" + str(self.getTravelTime()) + "h)"