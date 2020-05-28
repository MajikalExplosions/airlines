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

        for row in range(38):
            rowList = []
            for col in range(6):
                rowList.append(True)

            self.seats.append(rowList)

    def serialize(self):
        readFile = open("reservations/data_reservation/single_flights.txt", "r")
        flightStartInd = self.__fileContainsFlight(readFile.readlines())
        readFile.close()

        #means that this reservation has not already been serialized
        if flightStartInd == -1:
            reservationFile = open("reservations/data_reservation/single_flights.txt", "a")
            print(self.toString(), file=reservationFile)

        #it has been serialized and we have to override it
        else:
            pass

    #searches the list of file lines to see if it contains this flight
    #if it does, returns the line where the glith starts
    #if it doesn't, returns -1
    def __fileContainsFlight(self, fileLines):
        lineNum = 0

        while lineNum < len(fileLines):
            curLine = fileLines[lineNum]

            if curLine.find("Flight ID: ") != -1:
                flightID = curLine.lstrip("Flight ID: ")

                if flightID == self.flightId:
                    depLine, arrLine = fileLines[lineNum - 2].lstrip("Departure Date: "), fileLines[lineNum - 1].lstrip("Arrival Date: ")
                    if depLine == self.depDate and arrLine == self.arrDate:
                        return lineNum - 3
            else:
                lineNum += 1
        return -1

    def getFlightID(self):
        return self.flightId

    def bookSeat(self, row, col):
        self.seats[row][col]

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