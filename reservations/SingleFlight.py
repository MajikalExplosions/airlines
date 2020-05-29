# Name: SingleFlight.py
# Description: Class to represent a single, specific flight

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/26/20        Original

from flights import Flight

class SingleFlight:
    def __init__(self):
        #makes a list of all seat combinations of rows from 1-38 and letters from A-F
        self.seats = []

        for row in range(38):
            rowList = []
            for col in range(6):
                rowList.append(True)

            self.seats.append(rowList)

    def create(self, flight, depDate):
        self.depDate = depDate

        self.flightId = flight.getID()
        self.airline = flight.getAirline()
        self.number = flight.getNumber()
        self.origin = flight.getOrigin().toString()
        self.destination = flight.getDestination().toString()
        self.departureTime = flight.getDepTime()
        self.arrivalTime = flight.getArrTime()

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
                    depLine = fileLines[lineNum - 2].lstrip("Departure Date: ")
                    if depLine == self.depDate:
                        return lineNum - 3
            else:
                lineNum += 1
        return -1

    def getFlightID(self):
        return self.flightId

    def getDepartureTime(self):
        return self.departureTime

    def getArrivalTime(self):
        return self.arrivalTime

    def getDepartureDate(self):
        return self.depDate

    def getOrigin(self):
        return self.origin

    def getDestination(self):
        return self.destination

    def getAirline(self):
        return self.airline

    def getNumber(self):
        return self.number

    def bookSeat(self, row, col):
        self.seats[row][col] = True

    def getAvailableSeats(self):
        return self.seats

    def createFromID(self, id):
        readFile = open("reservations/data_reservation/single_flights.txt", "r")

        for line in readFile:
            if line.find(id) != -1:
                self.createFromString(line)

        readFile.close()

    def createFromString(self, string):
        tokens = string.split("  ")

        self.depDate = tokens[1].lstrip("Departure Date: ")
        self.flightId = tokens[2].lstrip("Flight ID: ")
        self.airline = tokens[3].lstrip("Airline: ")
        self.number = tokens[4].lstrip("Number: ")
        self.origin = tokens[5].lstrip("Origin: ")
        self.destination = tokens[6].lstrip("Destination: ")
        self.departureTime = tokens[7].lstrip("Departure Time: ")
        self.arrivalTime = tokens[8].lstrip("Arrival Time: ")

        seatList = tokens[9].lstrip("Booked Seats: ")
        for seat in seatList.split(" "):
            row, col = seat.split(",")
            self.seats[row][col] = True

    def toString(self):
        string = "Flight"
        string += "  Departure Date: " + str(self.depDate)
        string += "  Flight ID: " + str(self.flightId)
        string += "  Airline: " + str(self.airline)
        string += "  Number: " + str(self.number)
        string += "  Origin: " + str(self.origin)
        string += "  Destination: " + str(self.destination)
        string += "  Departure Time: " + str(self.departureTime)
        string += "  Arrival Time: " + str(self.arrivalTime)
        string += "  Booked Seats: "

        for row in range(38):
            for col in range(6):
                if self.seats[row][col]:
                    string += str(row) + "," + str(col)

        return string