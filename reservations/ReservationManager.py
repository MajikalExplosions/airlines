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
        for reservation in self.reservations:
            if reservation.getConfirmationNumber() == confirmationNumber and reservation.getLastName() == lastName:
                return reservation

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
        passengerInd = reservationStartInd
        while fileLines[passengerInd].find("Passenger") == -1:
            passengerInd += 1

        while fileLines[passengerInd].find("}") == -1:
            lastNameFile = fileLines[passengerInd].split("  ")[2].lstrip("Last Name: ")

            if lastNameFile == lastName:
                return True

            passengerInd += 1

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
            lineNum += 1
        return -1

    def validateCreditCard(self, creditCardNum):
        if not (16 <= len(creditCardNum) <= 19):
            return False

        try:
            creditCardNum = int(creditCardNum)

            if creditCardNum <= 0:
                return False
        except:
            return False

        #check digit is the last digit of the number
        checkDigit = creditCardNum % 10

        #creates a backwards list of the digits of the number except the check digit
        sequence = self.__splitNumToList(creditCardNum // 10)

        digitSum = 0

        #iterates through list right to left and adds each digit to the digit sum
        for i in range(len(sequence)):
            #for every other digit, multiplies by 2 and then turns that number into the sum of it's digits
            if i % 2 == 0:
                digit = sequence[i] * 2
                digit = (digit % 10) + (digit // 10)
            else:
                digit = sequence[i]

            digitSum += digit

        digitSum *= 9

        #if the last digit of the sum is the same as the last digit of the original, it's valid
        return (digitSum % 10) == checkDigit


    #takes a number and splits it into a list of each of it's digits, the returned list will be the number reversed
    def __splitNumToList(self, number):
        list = []

        while number > 0:
            list.append(number % 10)
            number //= 10

        return list
