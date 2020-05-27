# Name: FlightSearcher.py
# Description: Searches a flightmanager for flights

# Ver.	Writer			    Date			Notes
# 1.0   Joseph Liu			05/25/20		Original airport search ported from FlightManager, create searchForFlights
# 1.1   Joseph Liu			05/25/20		Add example code
# 1.2   Chris Luey			05/27/20		Add lookup


from flights.FlightManager import FlightManager
from flights.paths.Graph import Graph
from flights.paths.YenKSP import YenKSP


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

    def searchForFlights(self, origin, dest, k):
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

    def lookup(self, dest, flightnum):
        for flight in self.flightManager.getFlights():
            if flight.getDestination().getCode() == dest and flight.getNumber() == int(flightnum):
                return flight
        return "Flight {} to {} Doesn't Exist".format(flightnum, dest)

    def isValidAirport(self, s):
        for airport in self.flightManager.getAirports():
            if airport.getCode() == s:
                return True
        return False


def test_search():
    fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    fs = FlightSearcher(fm)
    inp = ""
    while inp != "quit":
        inp = input(">>> ").lower()
        t = inp.split()
        try:
            if t[0] == "search":
                if t[1] == "airport":
                    for airport in fs.searchForAirports(t[2]):
                        print(airport.toString())
                elif t[1] == "flight":
                    if len(t) == 4:
                        t.append(5)
                    for airport in \
                            fs.searchForFlights(fs.searchForAirports(t[2])[0], fs.searchForAirports(t[3])[0],
                                                int(t[4]))[
                                0].toFlights(fm):
                        print(airport.toString())
        except IndexError:
            print("Invalid command")
