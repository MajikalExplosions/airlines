# Name: Flight.py
# Description: Stores data for a single flight

# Ver.	Writer			    Date			Notes
# 0.1   Kyler Rosen         05/09/20		Add flight info from file except days
# 0.2   Joseph Liu			05/15/20		Renaming, add parsing for days, add travel time

import Time

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
        #Some times are written in the format 04:00+/-1, but I have no idea what the -1 is so for now I just cut it out.
        if self.arrivalTime.find("-") != -1 or self.arrivalTime.find("+") != -1:
            self.arrivalTime = self.arrivalTime[:-2]

        if self.departureTime.find("-") != -1 or self.departureTime.find("+") != -1:
            self.departureTime = self.departureTime[:-2]
        
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

    def getArrTime(self):
        return self.arrivalTime
    
    def getTravelTime(self):
        td = (Time.toUTC(self.destination.getTimezone(), Time.flightToDatetime(self.arrivalTime)) - Time.toUTC(self.origin.getTimezone(), Time.flightToDatetime(self.departureTime)))
        #td.total_seconds / 3600
        return (td.total_seconds() / 3600) % 24
    
    def toString(self):
        return "Flight " + self.airline + str(self.number) + " from " + self.origin.getSearchString() + " to " + self.destination.getSearchString() + " (" + str(self.getTravelTime()) + "h)"