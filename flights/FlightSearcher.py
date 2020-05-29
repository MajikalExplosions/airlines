# Name: FlightSearcher.py
# Description: Searches a flightmanager for flights

# Ver.	Writer			    Date			Notes
# 1.0   Joseph Liu			05/25/20		Original airport search ported from FlightManager, create searchForFlights
# 1.1   Joseph Liu			05/25/20		Add example code
# 1.2   Chris Luey			05/27/20		Add searchForFlight() Add isValidAirport()


from flights.FlightManager import FlightManager
from flights.paths.Graph import Graph
from flights.paths.YenKSP import YenKSP
from flights.Time import *

class FlightSearcher:
    def __init__(self, fm):
        self.flightManager = fm
        self.graph = Graph()
        self.graph.fromFlights(fm)
        self._flightCache = {}

    def searchForAirports(self, searchString):
        fullMatch, partMatch = [], []
        searchString = searchString.lower()
        for airport in self.flightManager.getAirports():
            details = [airport.getCode().lower(), airport.getCity().lower(), airport.getName().lower(),
                       airport.toString().lower()]

            match = False
            for d in details:
                if d == searchString and not match:
                    fullMatch.append(airport)
                    match = True
                    break

            for d in details:
                if not match and d.find(searchString) != -1:
                    partMatch.append(airport)
                    match = True
                    break

            if len(fullMatch) == 10:
                return fullMatch

        return fullMatch + partMatch[:10 - len(fullMatch)]

    def searchForFlights(self, origin, dest, k, y, m, d):
        setStartDate(y, m, d)
        c1, c2 = origin.getCode(), dest.getCode()
        if c1 + c2 in self._flightCache:
            search = self._flightCache[c1 + c2]
        else:
            search = YenKSP(self.graph, self.graph.getNodeFromAirport(origin), self.graph.getNodeFromAirport(dest))
            self._flightCache[c1 + c2] = search

        res = []
        for i in range(k):
            res.append(search.getPath(i))
        return res

    def searchForFlight(self, destinationCode, flightNumber):
        for flight in self.flightManager.getFlights():
            if flight.getDestination().getCode() == destinationCode and flight.getAirline() + str(
                    flight.getNumber()) == flightNumber:
                return flight
            if flight.getDestination().getCode() == destinationCode and str(flight.getNumber()) == flightNumber:
                return flight
        return "Flight {} to {} Doesn't Exist".format(flightNumber, destinationCode)

    def isValidAirport(self, s):
        for airport in self.flightManager.getAirports():
            if airport.getCode() == s:
                return True
        return False