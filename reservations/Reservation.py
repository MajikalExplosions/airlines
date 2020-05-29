# Name: Reservation.py
# Description: Class to hold an airline reservation

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/08/20        Original

from random import randrange
from reservations.Passenger import Passenger
from reservations.SingleFlight import SingleFlight

class Reservation:
    def __init__(self):
        self.confirmationNumber = ""

        self.passengers = []
        self.flights = []

    def getLastName(self):
        return self.passengers[0].getLastName()

    #parses a reservation string and returns a reservation object
    def createFromFile(self, fileLines, index):
        self.confirmationNumber = fileLines[index + 1].lstrip("Confirmation Number:")

        index += 2
        while fileLines[index].find("Flight") != -1:
            flight = SingleFlight(None, "", "")
            flight.createFromString(fileLines[index])
            self.flights.append(flight)
            index += 1

        while fileLines[index].find("Passenger") != -1:
            passenger = Passenger("", "", "")
            passenger.createFromString(fileLines[index])
            self.passengers.append(passenger)
            index += 1

    def setConfirmationNumber(self, confirmationNumber):
        self.confirmationNumber = confirmationNumber

    def addFlight(self, flight, depDate, arrDate):
        singleFlight = SingleFlight()
        singleFlight.create(flight, depDate, arrDate)
        self.flights.append(singleFlight)

    def addPassenger(self, passenger):
        self.passengers.append(passenger)

    def addSeat(self, seat, passengerFirstName, passengerLastName, flightID):
        for passenger in self.passengers:
            if passenger.getFirstName() == passengerFirstName and passenger.getLastName() == passengerLastName:
                passenger.addSeat(seat)

                for flight in self.flights:
                    if flight.getFlightID() == flightID:
                        flight.bookSeat(seat)

    def modifySeat(self, seat, passengerFirstName, passengerLastName, flightID):
        pass

    def getPassengers(self):
        return self.passengers

    def getAvailableSeatsByID(self, flightID):
        for flight in self.flights:
            if flight.getFlightID() == flightID:
                return flight.getAvailableSeats()

    def getFlights(self):
        return self.flights

    def getConfirmationNumber(self):
        if self.confirmationNumber != "":
            self.__issueConfirmationNumer()

        return self.confirmationNumber

    def serialize(self):
        if self.confirmationNumber == "":
            self.__issueConfirmationNumer()

        readFile = open("reservations/data_reservation/reservations.txt", "r")
        fileLines = readFile.readlines()
        reservationStartInd = self.__fileContainsConfirmationNumber(self.confirmationNumber, fileLines)
        readFile.close()

        #means that this reservation has not already been serialized
        if reservationStartInd == -1:
            reservationFile = open("reservations/data_reservation/reservations.txt", "a")
            print(self.__toString(), file=reservationFile)

        #it has been serialized and we have to override it
        else:
            endInd = reservationStartInd
            while fileLines[endInd].strip() != "":
                endInd += 1

            reservationFile = open("reservations/data_reservation/reservations.txt", "w")

            for i in range(len(fileLines)):
                if i < reservationStartInd and i >= endInd:
                    print(fileLines[i], file=reservationFile)

            print(self.__toString(), file=reservationFile)



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

    #takes a number and splits it into a list of each of it's digits, the returned list will be the number reversed
    def __splitNumToList(self, number):
        list = []

        while number > 0:
            list.append(number % 10)
            number //= 10

        return list

    def __issueConfirmationNumer(self):
        readFile = open("reservations/data_reservation/confirmation_numbers.txt", "r")

        #continuously generates a new number until we get one that has not already been issued
        confirmationNumber = self.__generateRandomConfirmation()
        while self.__fileContainsString(readFile, confirmationNumber):
            confirmationNumber = self.__generateRandomConfirmation()

        readFile.close()
        self.confirmationNumber = confirmationNumber

        #stores the issued code in a file to prevent future repeats
        confirmationFile = open("reservations/data_reservation/confirmation_numbers.txt", "a")
        print(confirmationNumber, file=confirmationFile)
        confirmationFile.close()

    def __fileContainsString(self, file, string):
        file.seek(0)

        for line in file:
            if string in line:
                return True

        return False

    def __generateRandomConfirmation(self):
        allChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d",
                    "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                    "y", "z"]
        confirmation = ""

        #makes 6 random selections to create the confirmation number
        for i in range(6):
            confirmation += allChars[randrange(len(allChars))]

        return confirmation

    def __toString(self):
        string = "Reservation {\n"
        string += "Confirmation Number: " + self.confirmationNumber + "\n"

        for flight in self.flights:
            string += flight.toString()

        for passenger in self.passengers:
            string += passenger.toString()

        string += "}\n"

        return string

