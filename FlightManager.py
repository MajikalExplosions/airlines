# Name: FlightManager.py
# Description: Route map manager

# Ver.	Writer			    Date			Notes
# 0.1   Kyler Rosen         05/09/20		File I/O test

class FlightManager:
	def __init__(self,file):
		file = open(file,"r")

		flights = file.readlines()[1:]

		print(flights[2])

		file.close()

	def getFlights(self):
		pass

	def getFlightsFrom(self):
		pass


def test():
	FlightMan = FlightManager("Flight Data - All Flights.csv")

if __name__ == '__main__':
	test()