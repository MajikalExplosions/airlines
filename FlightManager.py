# Name: FlightManager.py
# Description: Route map manager

# Ver.	Writer			    Date			Notes
# 0.1   Kyler Rosen         05/09/20		File I/O test
# 0.2   Joseph Liu			05/15/20		Add useful functions
# 0.3   Joseph Liu			05/15/20		Add file I/O with new data format

from Airport import Airport
from Flight import Flight

class FlightManager:
	def __init__(self, airportFile, flightFile):
		self.flights = []
		self.airports = []
		codes = {}
		processed = ""

		af = open(airportFile, "r")
		contents = af.readlines()[1:]
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
		contents = ff.readlines()[1:]
		ff.close()
		index = 0
		for line in contents:
			l = line.split("\t")
			for i in range(len(l)):
				l[i] = l[i].strip()
			if processed == l[4] + l[5]:
				continue
			processed = l[4] + l[5]
			#print(processed)
			self.flights.append(Flight(index, l[4], int(l[5]), self.airports[codes[l[0]]], self.airports[codes[l[1]]], l[2], l[3], l[6]))
			self.flights[-1].getOrigin().addFlight(self.flights[-1])
			self.flights[-1].getDestination().addFlight(self.flights[-1])
			index += 1
		
		n = []
		for a in self.airports:
			if a.hasFlight():
				n.append(a)
		self.airports = n
			

	def getFlights(self):
		return self.flights

	def getAirports(self):
		return self.airports


def test():
	FlightMan = FlightManager("airports.tsv", "flights.tsv")
	print("Flights from", FlightMan.airports[420].getName(), "\n")
	for f in FlightMan.airports[420].getFlights():
		print(f.toString())
	print("\n\nFlights from", FlightMan.airports[69].getName(), "\n")
	for f in FlightMan.airports[69].getFlights():
		print(f.toString())

if __name__ == '__main__':
	test()