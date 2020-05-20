# Name: FlightManager.py
# Description: Route map manager

# Ver.	Writer			    Date			Notes
# 0.1   Kyler Rosen         05/09/20		File I/O test
# 0.2   Joseph Liu			05/15/20		Add useful functions
# 0.3   Joseph Liu			05/15/20		Add file I/O with new data format
# 0.4 	Kyler Rosen 		05/20/20		Added searchAirport, sorts the airports

from Airport import Airport
from Flight import Flight

def getFlightNum(airport):
	return airport.getFlightNum()

class FlightManager:
	def __init__(self, airportFile, flightFile):
		self.flights = []
		self.airports = []
		codes = {}

		af = open(airportFile, "r")
		contents = af.readlines()
		af.close()
		index = 0
		for line in contents:
			l = line.split("\t")
			for i in range(len(l)):
				l[i] = l[i].strip()
			self.airports.append(Airport(l[0], l[3], l[2], l[1]))
			codes[self.airports[-1].getCode()] = index
			index += 1
		
		ff = open(flightFile, "r")
		contents = ff.readlines()
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
		
		n = []
		for a in self.airports:
			if a.hasFlight():
				n.append(a)
		self.airports = n

		self.airports.sort(key = getFlightNum, reverse = True)
		
		print("Done processing. Flights:", len(self.flights), "| Airports:", len(self.airports))
			

	def getFlights(self):
		return self.flights

	def getAirports(self):
		return self.airports

	def searchAirport(self,string):
		matchingAirports = []
		for airport in self.airports:
			if len(string) == 3 and airport.getCode().lower() == string.lower():
				matchingAirports.append(airport)

			if airport.getCity().lower() == string.lower():
				matchingAirports.append(airport)

			if airport.getName().lower() == string.lower():
				matchingAirports.append(airport)

			if airport.getSearchString().lower() == string.lower():
				matchingAirports.append(airport)

			if len(matchingAirports) == 10:
				return matchingAirports

		for airport in self.airports:
			if (len(string) <= len(airport.getCity())) and (airport.getCity()[:len(string)].lower() == string.lower()) and not airport in matchingAirports:
		 		matchingAirports.append(airport)

			if len(string) <= len(airport.getSearchString()) and airport.getSearchString()[:len(string)].lower() == string.lower() and not airport in matchingAirports:
				matchingAirports.append(airport)

			if len(matchingAirports) == 10:
				return matchingAirports

		return matchingAirports


def test():
	FlightMan = FlightManager("airports.tsv", "flights.tsv")
	

	print("Flights from", FlightMan.airports[0].getName(), "\n")
	for f in FlightMan.airports[0].getFlights():
	 	print(f.toString())
	print("\n\nFlights from", FlightMan.airports[1].getName(), "\n")
	for f in FlightMan.airports[1].getFlights():
	 	print(f.toString())

	for airport in FlightMan.airports[0:10]:
		print(airport.getSearchString())
		print(airport.getFlightNum())


	airports = FlightMan.searchAirport("SAN")

	for airport in airports:
		print(airport.getSearchString())
		print(airport.getFlightNum())

if __name__ == '__main__':
	test()