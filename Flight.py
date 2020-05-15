class Flight:
	def __init__(self, id, airline, num, origin, destination, depTime, arrTime, days):
		self.id = id 
        self.airline = airline
        self.number = num
        self.origin = origin
        self.destination = destination
        self.departureTime = depTime
        self.arrivalTime = arrTime

    def getID(self):
    	return self.id

    def getAirline(self):
    	return self.airline
        
    def getNumber(self):
        return self.number

    def getOrigin(self):
        return self.orig

    def getDestination(self):
        return self.dest

    def getDepTime(self):
        return self.depTime

    def getArrTime(self):
        return self.arrTime
