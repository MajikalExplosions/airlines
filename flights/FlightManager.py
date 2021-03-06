# Name: FlightManager.py
# Description: Route map manager

# Ver.	Writer			    Date			Notes
# 0.1   Kyler Rosen         05/09/20		File I/O test
# 0.2   Joseph Liu			05/15/20		Add useful functions
# 0.3   Joseph Liu			05/15/20		Add file I/O with new data format
# 0.4 	Kyler Rosen 		05/20/20		Added searchAirport, sorts the airports
# 1.0 	Joseph Liu	 		05/25/20		General cleanup and moved search to flightsearcher

from flights.Airport import Airport
from flights.Flight import Flight

class FlightManager:
	def __init__(self, airportFile, flightFile):
		self.flights = []
		self.airports = []
		codes = {}
		
		#creates airport list
		af = open(airportFile, "r")
		contents = af.readlines()[1:]
		af.close()
		index = 0
		for line in contents:
			l = line.split("\t")
			for i in range(len(l)):
				l[i] = l[i].strip()
			self.airports.append(Airport(l[0], l[3], l[2], l[1], int(l[4])))
			codes[self.airports[-1].getCode()] = index
			index += 1
		
		#creates flight list
		ff = open(flightFile, "r")
		contents = ff.readlines()[1:]
		ff.close()
		index = 0
		for line in contents:
			l = line.split("\t")
			for i in range(len(l)):
				l[i] = l[i].strip()
			self.flights.append(Flight(index, l[4], int(l[5]), self.airports[codes[l[0]]], self.airports[codes[l[1]]], l[2], l[3], l[6]))
			self.flights[-1].getOrigin().addFlight(self.flights[-1])
			self.flights[-1].getDestination().addFlight(self.flights[-1])
			index += 1

		self.airports.sort(key = fm_getFlightNum,reverse = True)

		for index in range(len(self.airports)):
			self.airports[index].assignId(index)
		
		print("Done processing. Flights:", len(self.flights), "| Airports:", len(self.airports))
			

	def getFlights(self):
		return self.flights

	def getAirports(self):
		return self.airports

	def getAirport(self, accessNum):
		return self.airports[accessNum]

def fm_getFlightNum(airport):
	return airport.getFlightNum()