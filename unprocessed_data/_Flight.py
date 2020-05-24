# Name: flights.py
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
        self.days = days

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
        return (td.total_seconds() / 3600) % 24

    
    def toString(self):
        return "flights " + self.airline + str(self.number) + " from " + self.origin.getSearchString() + " to " + self.destination.getSearchString() + " (" + str(self.getTravelTime()) + "h)"