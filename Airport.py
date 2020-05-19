# Name: Airport.py
# Description: Stores data for a single airport

# Ver.	Writer			    Date			Notes
# 0.1   Kyler Rosen         05/09/20		Add airport code, city, and timezone
# 0.2   Joseph Liu			05/15/20		Add flight data storage for graph
# 0.3   Joseph Liu			05/15/20		Add name info for searching

class Airport:
	def __init__(self, code, city, name, timezone):
		self.code = code
		self.city = city
		self.name = name
		self.timezone = timezone
		self.flights = []
		self.node = 0
		self.serviced = False

	def addFlight(self, f):
		self.serviced = True
		if f.getOrigin() == self:
			self.flights.append(f)

	def getFlights(self):
		return self.flights

	def getCode(self):
		return self.code

	def getCity(self):
		return self.city

	def getTimezone(self):
		return self.timezone

	def setNode(self, n):
		self.node = n
	
	def getNode(self):
		return self.node
	
	def hasFlight(self):
		return self.serviced
	
	def getName(self):
		return self.name + ", " + self.city
	
	def getSearchString(self):
		return self.name + ", " + self.city + " (" + self.code + ")"