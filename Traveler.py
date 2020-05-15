# Name: Traveler.py
# Description: Info about a single traveler

# Ver.	Writer			        Date			Notes
# 1.0     Shuvam Chatterjee     05/10/20		Original

class Traveler:
    def __init__(self, firstName, lastName, birthDate, gender):
        self.firstName = firstName
        self.lastName = lastName
        self.birthDate = birthDate
        self.gender = gender

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.lastName

    def getBirthDate(self):
        return self.birthDate

    def getGender(self):
        return self.gender
