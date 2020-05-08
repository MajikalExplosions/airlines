# Name: Reservation.py
# Description: Class to hold an airline reservation

# Ver.	Writer			        Date			Notes
# 1.0     Shuvam Chatterjee     05/08/20		Original

import random

class Reservation:
    def validateCreditCard(self, creditCardNum, cardCompany, pinCode):
        pass

    def issueConfirmationNumer(self):
        usedNumbers = open("confirmationNumbers.txt", "r")

        confirmationNumber = self.__generateRandomConfirmation()
        while self.__fileContainsString(usedNumbers, confirmationNumber):
            confirmationNumber = self.__generateRandomConfirmation()

        usedNumbers.close()

        confirmationFile = open("confirmationNumbers.txt", "a")
        print(confirmationNumber, file=confirmationFile)
        confirmationFile.close()

        return confirmationNumber

    def __fileContainsString(self, file, string):
        file.seek(0)

        for line in file:
            if string in line:
                return True
        return False

    def __generateRandomConfirmation(self):
        allCharacters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        confirmation = ""

        for i in range(6):
            confirmation += allCharacters[random.randrange(len(allCharacters))]

        return confirmation

Reservation().issueConfirmationNumer()
