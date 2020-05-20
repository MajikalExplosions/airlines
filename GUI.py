# Name: GUI.py
# Description: File for GUI and screens

# Ver.	       Writer			 Date			Notes
# 1.0     Christopher Luey     05/08/20		    Master
# 1.1     Christopher Luey     05/15/20	   Add switchScreen method

from Button import *

class GUI:

    def __init__(self):
        self.win = GraphWin(title="Airport", width=1200, height=800, autoflush=False)
        self.main = Screen('main', self.win)
        self.start = Screen('start', self.win)
        self.create_reservation = Screen('create_reservation', self.win)
        self.modify_reservation = Screen('modify_reservation', self.win)
        self.flight_status = Screen('flight_status', self.win)
        self.checkin = Screen('checkin', self.win)
        self.previousScreen = self.main

        self.inflate_header()
        self.activeScreen = self.main
        self.attrs = self.activeScreen.inflate()


    def switchScreen(self, screen):

        """
        Args:
            screen:
        """
        if screen == "main":
            if self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.previousScreen = self.activeScreen
            self.activeScreen = self.main
            self.attrs = self.activeScreen.inflate()
            pass
        elif screen == "create_reservation":
            if not self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.previousScreen = self.activeScreen
            self.activeScreen = self.create_reservation
            self.attrs = self.activeScreen.inflate()
            pass
        elif screen == "modify_reservation":
            if not self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.previousScreen = self.activeScreen
            self.activeScreen = self.modify_reservation
            self.attrs = self.activeScreen.inflate()
            pass
        elif screen == "flight_status":
            if not self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.previousScreen = self.activeScreen
            self.activeScreen = self.flight_status
            self.attrs = self.activeScreen.inflate()
            pass
        elif screen == "checkin":
            if not self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.previousScreen = self.activeScreen
            self.activeScreen = self.checkin
            self.attrs = self.activeScreen.inflate()
            pass
        elif screen == "start":
            if not self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.previousScreen = self.activeScreen
            self.activeScreen = self.start
            self.attrs = self.activeScreen.inflate()
            pass
        elif screen == "back":
            if self.previousScreen == self.main and self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.previousScreen, self.activeScreen = self.activeScreen, self.previousScreen
            self.attrs = self.activeScreen.inflate()
        else:
            raise("Could not locate screen")
        print("Switching to screen", self.activeScreen.getName())

    def getScreen(self):
        return self.activeScreen


    def setOnButtonClickListener(self):
        p = self.win.getMouse()
        buttons = {"Modify an Existing Reservation" : "modify_reservation",
                   "Create a Reservation" : "create_reservation",
                   "Lookup Flight Status" : "flight_status",
                   "Check-In Online" : "checkin"}
        while not self.quitButton.isClicked(p):
            for i in self.attrs:
                if type(i) == Button and i.isClicked(p):
                    return buttons[i.getText()]
            if self.backButton.isClicked(p):
                return 'back'
            p = self.win.getMouse()
        return 'quit'


    def inflate_header(self):
        self.home = Button(595, 75/2 - 5, 1205, 80, 0, color_rgb(8, 76, 97), 'ᴀɪʀᴘᴏʀᴛ ᴘʀᴏɢʀᴀᴍ', 'white', 26, self.win)
        self.home.setInactiveColor(color_rgb(8, 76, 97))
        self.home.toggleActivation()
        self.home.toggleActivation()
        self.quitButton = Button(1125, 75 / 2, 100, 50, 5, color_rgb(219, 80, 74), "Exit", 'white', 20, self.win)
        self.quitButton.toggleActivation()
        self.backButton = Button(75, 75 / 2, 100, 50, 5, color_rgb(219, 80, 74), "Back", 'white', 20, self.win)

class Screen:

    def __init__(self, name, win):
        """
        Args:
            name:
            win:
        """
        self.name = name
        self.win = win
        path = "Screens/" + name + ".txt"
        try:
            self.source_file = open(path, 'r')
            self.attr = self._parse(self.source_file)
        except:
            raise("Could not locate file: " + path)



    def deflate(self):
        for i in self.attr:
            if type(i) == Button:
                i.toggleActivation()
            i.undraw()

    def inflate(self):
        for i in self.attr:
            if type(i) == Button:
                if not i.isDrawn():
                    i.draw(self.win)
                if not i.isActive():
                    i.toggleActivation()
            else:
                i.draw(self.win)
        return self.attr

    def getName(self):
        return self.name

    def _parse(self, s):

        """
        Args:
            s:
        """
        attrs = []
        source = s.readlines()
        if source:
            self.background = source[0].rstrip("Background: ")
            i=2
            while i < len(source):
                if source[i][0] == "<" and source[i].lstrip("<").rstrip(">\n") == "Button":
                    attrs.append(Button(float(source[i+1].lstrip("x: ").rstrip("\n")), float(source[i+2].lstrip("y: ").rstrip("\n")), float(source[i+3].lstrip("width: ").rstrip("\n")), float(source[i+4].lstrip("height: ").rstrip("\n")), float(source[i+5].lstrip("radius: ").rstrip("\n")), color_rgb(int(source[i+6].lstrip("color: ").rstrip("\n").strip().split(",")[0]), int(source[i+6].lstrip("color: ").rstrip("\n").strip().split(",")[1]), int(source[i+6].lstrip("color: ").rstrip("\n").strip().split(",")[2])), str(source[i+7].lstrip("text: ").rstrip("\n")), color_rgb(int(source[i+8].lstrip("textColor: ").rstrip("\n").strip().split(",")[0]), int(source[i+8].lstrip("textColor: ").rstrip("\n").strip().split(",")[1]), int(source[i+8].lstrip("textColor: ").rstrip("\n").strip().split(",")[2])), int(source[i+9].lstrip("textSize: ").rstrip("\n")), self.win))
                    i+=12
                #elif source[i].rstrip("<").lstrip(">\n") == "Attr":
        return attrs
