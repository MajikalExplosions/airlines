# Name: Reservation.py
# Description: Class to hold an airline reservation

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/08/20        Original

import random

class Reservation:
    def validateCreditCard(self, creditCardNum):
        #check digit is the last digit of the number
        checkDigit = creditCardNum % 10

        #creates a backwards list of the digits of the number except the check digit
        sequence = self.__splitNumToList(creditCardNum // 10)

        digitSum = 0

        #iterates through list and adds each digit to the digit sum
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
        #continuously generates a new number until we get one that has not already been issued
        confirmationNumber = self.__generateRandomConfirmation()
        while self.__fileContainsString("confirmationNumbers.txt", confirmationNumber):
            confirmationNumber = self.__generateRandomConfirmation()

        self.confirmationNumber = confirmationNumber

        #stores the issued code in a file to prevent future repeats
        confirmationFile = open("confirmationNumbers.txt", "a")
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
            confirmation += allChars[random.randrange(len(allChars))]

        return confirmation

    def getConfirmationNumber(self):
        return self.confirmationNumber
