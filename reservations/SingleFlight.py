# Name: SingleFlight.py
# Description: Class to represent a single, specific flight

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/26/20        Original

from flights import Flight

class SingleFlight:
    def __init__(self, flight, depDate, arrDate):
        self.depDate = depDate
        self.arrDate = arrDate

        self.flightId = flight.getId()
        self.airline = flight.getAirline()
        self.number = flight.getNumber()
        self.origin = flight.getOrigin().toString()
        self.destination = flight.getDestination().toString()
        self.departureTime = flight.getDepTime()
        self.arrivalTime = flight.getArrTime()

        #makes a list of all seat combinations of rows from 1-38 and letters from A-F
        self.seats = []

        for row in range(1, 39):
            for letter in range(65, 71):
                self.seats.append(str(row) + chr(letter))

    def bookSeat(self, seat):
        self.seats.remove(seat)

    def getAvailableSeats(self):
        return self.seats

    def createFromString(self, string):
        tokens = string.split("  ")

        self.depDate = tokens[1].lstrip("Departure Date: ")
        self.arrDate = tokens[2].lstrip("Arrival Date: ")
        self.flightId = tokens[3].lstrip("Flight ID: ")
        self.airline = tokens[4].lstrip("Airline: ")
        self.number = tokens[5].lstrip("Number: ")
        self.origin = tokens[6].lstrip("Origin: ")
        self.destination = tokens[7].lstrip("Destination: ")
        self.departureTime = tokens[8].lstrip("Departure Time: ")
        self.arrivalTime = tokens[9].lstrip("Arrival Time: ")

    def toString(self):
        string = "Flight"
        string += "  Departure Date: " + self.depDate
        string += "  Arrival Date" + self.arrDate
        string += "  Flight ID: " + self.flightId
        string += "  Airline: " + self.airline
        string += "  Number: " + self.number
        string += "  Origin: " + self.origin
        string += "  Destination: " + self.destination
        string += "  Departure Time: " + self.departureTime
        string += "  Arrival Time: " + self.arrivalTime
        return string