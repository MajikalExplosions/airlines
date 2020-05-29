# Name: ReservationManager.py
# Description: Class to store all reservations

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/26/20        Original

from reservations.Reservation import *

class ReservationManager:
    def __init__(self):
        self.reservations = []
        self.singleFlights = []

    def createReservation(self):
        reservation = Reservation()
        self.reservations.append(reservation)
        return reservation

    def serializeAll(self):
        for reservation in self.reservations:
            reservation.serialize()

        for flight in self.singleFlights:
            flight.serialize()

    def loadReservation(self, confirmationNumber, lastName):
        readFile = open("reservations/data_reservation/reservations.txt", "r")
        fileLines = readFile.readlines()
        readFile.close()

        reservationStartInd = self.__fileContainsConfirmationNumber(confirmationNumber, fileLines)

        if reservationStartInd == -1:
            raise("Confirmation number was not found.")

        #fileContainsReservation only makes sure that the confirmation numbers match so we still need to check the last name
        if not self.__reservationMatchesLastName(lastName, fileLines, reservationStartInd):
            raise("Last name was not found.")

        reservation = Reservation()
        reservation.createFromFile(fileLines, reservationStartInd)

        return reservation

    def __reservationMatchesLastName(self, lastName, fileLines, reservationStartInd):
        passengerLastNameInd = reservationStartInd + 5

        while passengerLastNameInd < len(fileLines) and fileLines[passengerLastNameInd].find("Last Name: ") != -1:
            if fileLines[passengerLastNameInd].lstrip("Last Name: ") == lastName:
                return True

            passengerLastNameInd += 4

        return False

    #searches the list of file lines to see if it contains a reservation with the given confirmation number
    #if it does, returns the line where the reservation starts
    #if it doesn't, returns -1
    def __fileContainsConfirmationNumber(self, confirmationNumber, fileLines):
        lineNum = 0

        while lineNum < len(fileLines):
            curLine = fileLines[lineNum]

            if curLine.find("Confirmation Number: ") != -1:
                #the string "Confirmation Number: " has length 21 so everything after that is the actual number
                confirmationNum = curLine.lstrip("Confirmation Number: ")

                if confirmationNum == confirmationNumber:
                    #the start of a reservation will be 1 line above where it's confirmation number is
                    return lineNum - 1
            else:
                lineNum += 1
        return -1
