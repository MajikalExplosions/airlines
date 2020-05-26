# Name: SingleFlight.py
# Description: Class to represent a single, specific flight

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/26/20        Original

class SingleFlight:
    def __init__(self, flight, depDate, arrDate):
        self.flight = flight
        self.depDate = depDate
        self.arrDate = arrDate

        #makes a list of all seat combinations of rows from 1-38 and letters from A-F
        self.seats = []

        for row in range(1, 39):
            for letter in range(65, 71):
                self.seats.append(str(row) + chr(letter))

    def bookSeat(self, seat):
        self.seats.remove(seat)

    def getAvailableSeats(self):
        return self.seats