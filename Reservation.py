# Name: Reservation.py
# Description: Class to hold an airline reservation

# Ver.	Writer			        Date			Notes
# 1.0     Shuvam Chatterjee     05/08/20		Original

import random

class Reservation:
    def validateCreditCard(self, creditCardNum):
        #check digit is the last digit of the number
        checkDigit = creditCardNum % 10

        #creates a list of strings of all of the digits but the last one
        sequence = self.__splitNumToList(creditCardNum // 10)

        digitSum = 0

        for i in range(len(sequence)):
            #for every other digit, multiplies by 2 and then turns that number into the sum of it's digits
            if i % 2 == 0:
                digit = sequence[i] * 2
                digit = (digit % 10) + (digit // 10)
            else:
                digit = sequence[i]

            digitSum += digit

        digitSum *= 9

        return (digitSum % 10) == checkDigit

    #takes a number and splits it into a list of each of it's digits, the returned list will be the number reversed
    def __splitNumToList(self, number):
        list = []

        while number > 0:
            list.append(number % 10)
            number //= 10

        return list

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
