# File: 
# Written By: Christopher Luey
# Date: 
#

from graphics import *

class GUI:

    def __init__(self):
        self.win = GraphWin(title="Airport", width=1000, height=800, autoflush=False)
        main = Screen('main')
        self.activeScreen = main
        pass

    def switchScreen(self, screen):
        if screen == "MAIN":
            pass
        elif screen == "CREATE_RESERVATION":
            pass
        elif screen == "MODIFY_RESERVATION":
            pass
        elif screen == "FLIGHT_STATUS":
            pass
        elif screen == "CHECKIN":
            pass
        elif screen == "START":
            pass
        else:
            raise("unknown screen")

    def getScreen(self):
        return self.activeScreen

    def setButtonClickListener(self):


class Screen:

    def __init__(self, name, win):
        self.name = name
        self.win = win
        pass

    def undraw(self):

