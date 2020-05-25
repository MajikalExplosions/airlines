# Name: FlightSearcher.py
# Description: Searches a flightmanager for flights

# Ver.	Writer			    Date			Notes
# 0.1   Joseph Liu			05/25/20		Original airport search ported from FlightManager, create searchForFlights

from flights.FlightManager import FlightManager
from flights.Flight import Flight
from flights.paths.Graph import Graph
from flights.paths.YenKSP import YenKSP

def getFlightNum(airport):
	return airport.getFlightNum()

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
			if len(searchString) == 3 and airport.getCode().lower() == searchString:
				fullMatch.append(airport)
			details = [airport.getCity().lower(), airport.getName().lower(), airport.toString().lower()]

			match = False
			for d in details:
				if d == searchString:
					fullMatch.append(airport)
					match = True
					break
			
			for d in details:
				if not match and d.index(searchString) != -1:
					partMatch.append(airport)
					break
		
			if len(fullMatch) == 10:
				return fullMatch

		return fullMatch + partMatch[:10 - len(fullMatch)]
	
	def searchForFlights(self, origin, dest, k):
		c1, c2 = origin.getCode(), dest.getCode()
		if c1 + c2 in self._flightCache:
			search = self._flightCache(c1 + c2)
		else:
			search = YenKSP(self.graph, self.graph.getNodeFromAirport(origin), self.graph.getNodeFromAirport(dest))
		res = []
		for i in range(k):
			res.append(search.getPath(i))
		
		return res