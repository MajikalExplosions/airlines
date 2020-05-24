# Name: Passenger.py
# Description: Info about a single traveler

# Ver.	Writer			        Date			Notes
# 1.0     Shuvam Chatterjee     05/10/20		Original

class Passenger:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

        self.seats = []

    def addSeat(self, seat):
        self.seats.append(seat)

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.lastName

    def toString(self):
        string = "Passenger"
        string += " First Name: " + self.firstName
        string += " Last Name: " + self.lastName
        string += " Seats: " + str(self.seats)

        return string