# Name: reservation.py
# Description: Class to hold an airline reservation

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/08/20        Original

from random import randrange
from reservation.Passenger import Passenger

class Reservation:
    def __init__(self):
        self.confirmationNumber = ""
        self.passengers = []
        self.flights = []

    def loadFromFile(self, confirmationNumber, lastName):
        readFile = open("reservation/data_reservation/reservation.txt", "r")
        fileLines = readFile.readlines()
        reservationStartInd = self.__fileContainsConfirmationNumber(confirmationNumber, fileLines)

        if reservationStartInd == -1:
            return "Confirmation number was not found."

        #fileContainsReservation only makes sure that the confirmation numbers match so we still need to check the last name
        if not self.__reservationMatchesLastName(lastName, fileLines, reservationStartInd):
            return "Last name was not found."

        self.__parseReservation(fileLines, reservationStartInd)

        readFile.close()
        return "Loaded successfully."

    def serialize(self):
        if self.confirmationNumber == "":
            self.confirmationNumber = self.issueConfirmationNumer()

        readFile = open("reservation/data_reservation/reservation.txt", "r")
        reservationStartInd = self.__fileContainsConfirmationNumber(self.confirmationNumber, readFile.readlines())
        readFile.close()

        #means that this reservation has not already been serialized
        if reservationStartInd == -1:
            reservationFile = open("reservation/data_reservation/reservation.txt", "a")
            print(self.__toString(), file=reservationFile)

        #it has been serialized and we have to override it
        else:
            pass

    def __toString(self):
        string = "reservation {\n"
        string += "Confirmation Number: " + self.confirmationNumber + "\n"
        string += "flights: " + str(self.flights) + "\n"

        for passenger in self.passengers:
            string += passenger.toString()

        return string


    #parses a reservation and sets instance variables accordingly
    def __parseReservation(self, fileLines, index):
        self.confirmationNumber = fileLines[index + 1].lstrip("Confirmation Number:")

        #TODO: Do flight parsing



    def __createPassengerFromString(self, passengerString):
        firstName = passengerString[1].lstrip("First Name: ")
        lastName = passengerString[2].lstrip("Last Name: ")

        passenger = Passenger(firstName, lastName)

        seatsString = passengerString[3].lstrip("Seats: ")[1:-1]

        for seat in seatsString.split(","):
            passenger.addSeat(seat.strip())

        return passenger

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

    def addPassenger(self, firstName, lastName, birthDate, gender):
        self.passengers.append(Passenger(firstName, lastName, birthDate, gender))

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

    def issueConfirmationNumer(self):
        if self.confirmationNumber != "":
            return self.confirmationNumber

        #continuously generates a new number until we get one that has not already been issued
        self.confirmationNumber = self.__generateRandomConfirmation()
        while self.__fileContainsString("reservation/data_reservation/confirmation_numbers.txt", self.confirmationNumber):
            confirmationNumber = self.__generateRandomConfirmation()

        self.confirmationNumber = confirmationNumber

        #stores the issued code in a file to prevent future repeats
        confirmationFile = open("reservation/data_reservation/confirmation_numbers.txt", "a")
        print(confirmationNumber, file=confirmationFile)
        confirmationFile.close()

        return confirmationNumber

    def __fileContainsString(self, fileName, string):
        file = open(fileName, "r")

        for line in file:
            if string in line:
                file.close()
                return True

        file.close()
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

    def getConfirmationNumber(self):
        return self.confirmationNumber

    def getPassengers(self):
        return self.passengers