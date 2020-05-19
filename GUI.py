# Name: GUI.py
# Description: File for GUI and screens

# Ver.	       Writer			 Date			Notes
# 1.0     Christopher Luey     05/08/20		   Original


from graphics import *

class GUI:

    def __init__(self):
        self.win = GraphWin(title="Airport", width=1000, height=800, autoflush=False)
        main = Screen('main', self.win)
        self.activeScreen = main
        pass

    def switchScreen(self, screen):

        """
        Args:
            screen:
        """
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
            raise("Could not locate screen")

    def getScreen(self):
        return self.activeScreen


    def setOnButtonClickListener(self):
        pass

class Screen:

    def __init__(self, name, win):
        """
        Args:
            name:
            win:
        """
        self.name = name
        self.win = win
        path = "/Screens/" + name + ".txt"
        try:
            self.source_file = open(path, 'r')
            self.attr = self._parse(self.source_file)
        except:
            raise("Could not locate file: " + path)



    def undraw(self):
        pass

    def draw(self):
        pass

    def _parse(self, source):

        """
        Args:
            source:
        """
        pass


