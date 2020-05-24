# Name: BoardingPass.py
# Description: Class to create and output a boarding pass

# Ver.  Writer              Date            Notes
# 1.0   Shuvam Chatterjee   05/22/20        Original

class BoardingPass:
    def __init__(self, reservation):
        for passenger in reservation.getPassengers():
            pass