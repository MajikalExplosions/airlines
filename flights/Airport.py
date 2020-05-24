# Name: Airport.py
# Description: Stores data for a single airport

# Ver.	Writer			    Date			Notes
# 0.1   Kyler Rosen         05/09/20		Add airport code, city, and timezone
# 0.2   Joseph Liu			05/15/20		Add flight data storage for graph
# 0.3   Joseph Liu			05/15/20		Add name info for searching
# 0.4	Kyler Rosen			05/20/20		Cleaned up functions

class Airport:

	def __init__(self, code, city, name, timezone, size):
		self.code = code
		self.city = city
		self.name = name
		self.timezone = timezone
		self.flights = []
		self.flightNum = 0
		self.ID = -1
		
		if size > 2 or size < 0:
			size = 2
		self.size = size

	def getFlightNum(self):
		return self.flightNum


	def addFlight(self, f):
		if f.getOrigin() == self:
			self.flights.append(f)

		self.flightNum +=1

	def getFlights(self):
		return self.flights

	def getCode(self):
		return self.code

	def getCity(self):
		return self.city

	def getTimezone(self):
		return self.timezone
	
	def getName(self):
		return self.name + ", " + self.city
	
	def getSearchString(self):
		return self.name + ", " + self.city + " (" + self.code + ")"

	def assignId(self,ID):
		self.ID = ID

	def getID(self):
		return self.ID
