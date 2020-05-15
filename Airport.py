# Name: Airport.py
# Description: Stores data for a single airport

# Ver.	Writer			    Date			Notes
# 0.1   Kyler Rosen         05/09/20		Add airport code, city, and timezone
# 0.2   Joseph Liu			05/15/20		Add flight data storage for graph

class Airport:
	def __init(self, code, city, timezone):
		self.code = code
		self.city = city
		self.timezone = timezone
		self.flights = []

	def addFlight(self, f):
		self.flights.append(f)

	def getFlights(self):
		return self.flights

	def getCode(self):
		return self.code

	def getCity(self):
		return self.city

	def getTimezone(self):
		return self.timezone