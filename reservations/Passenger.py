# Name: Passenger.py
# Description: Info about a single traveler

# Ver.	Writer			        Date			Notes
# 1.0     Shuvam Chatterjee     05/10/20		Original
# 1.1     Chris Luey            05/27/20		Add age & mutator methods
# 1.2     Shuvam Chatterjee     05/28/20        Remove age parameter


class Passenger:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

        self.seats = []

    def setSeatAt(self, seat, index):
        self.seats[index] = seat

    def addSeat(self, seat):
        self.seats.append(seat)

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.lastName

    def setFirstName(self, first):
        self.firstName = first

    def setLastName(self, last):
        self.lastName = last

    def createFromString(self, string):
        tokens = string.split("  ")
        self.firstName = tokens[1].lstrip("First Name: ")
        self.lastName = tokens[2].lstrip("Last Name: ")

        seats = tokens[3].lstrip("Seats: [").rstrip("]")
        for seat in seats.split(", "):
            self.seats.append(seat)


    def toString(self):
        string = "Passenger"
        string += "  First Name: " + self.firstName
        string += "  Last Name: " + self.lastName
        string += "  Seats: " + str(self.seats)

        return string