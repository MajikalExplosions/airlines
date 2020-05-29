# Name: BoardingPass.py
# Description: Class to create and output a boarding pass

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/22/20        Original

from random import randint

class BoardingPass:
    def __init__(self, reservation):
        self.reservation = reservation
        self.export()

    def export(self):
        fileName = "reservations/boarding_passes/Reservation" + self.reservation.getConfirmationNumber() + ".txt"
        file = open(fileName, "w")

        flights = self.reservation.getFlights()
        string = ""
        for i in range(len(flights)):
            flight = flights[i]
            gate = randint(1, 8)

            for passenger in self.reservation.getPassengers():
                string += "NAME OF PASSENGER:\n"
                string += passenger.getLastName() + " / " + passenger.getFirstName() + "\n"
                string += "FROM: " + flight.getOrigin() + "\n"
                string += "TO: " + flight.getDestination() + "\n"
                string += "SEAT: " + passenger.getSeats()[i] + "\n"
                string += "GATE: " + str(gate) + "\n"
                string += "\n\n"

        print(string, file=file)

        file.close()

        return fileName