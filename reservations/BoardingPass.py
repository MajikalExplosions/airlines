# Name: BoardingPass.py
# Description: Class to create and output a boarding pass

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/22/20        Original

class BoardingPass:
    def __init__(self, reservation):
        self.reservation = reservation

    def export(self):
        fileName = "Reservation" + self.reservation.getConfirmationNumber() + ".txt"
        file = open(fileName, "w")

        for flight in self.reservation.getFlights():
            for passenger in self.reservation.getPassengers():
                string = passenger.getFirstName() + passenger.getLastName()

        return fileName