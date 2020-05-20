# Name: GUI.py
# Description: File for GUI and screens

# Ver.	       Writer			 Date			Notes
# 1.0     Christopher Luey     05/08/20		   Master


from Button import *
import time

class GUI:

    def __init__(self):
        self.win = GraphWin(title="Airport", width=1200, height=800, autoflush=False)
        main = Screen('main', self.win)
        start = Screen('start', self.win)
        create_reservation = Screen('create_reservation', self.win)
        modify_reservation = Screen('modify_reservation', self.win)
        flight_status = Screen('flight_status', self.win)
        checkin = Screen('checkin', self.win)

        self.inflate_header()
        self.activeScreen = main
        self.attrs = self.activeScreen.inflate()


    def switchScreen(self, screen):

        """
        Args:
            screen:
        """
        if screen == "main":
            pass
        elif screen == "create_reservation":
            pass
        elif screen == "modify_reservation":
            pass
        elif screen == "flight_status":
            pass
        elif screen == "checkin":
            pass
        elif screen == "start":
            pass
        else:
            raise("Could not locate screen")

    def getScreen(self):
        return self.activeScreen


    def setOnButtonClickListener(self):
        p = self.win.getMouse()
        buttons = {"Modify an Existing Reservation" : "modify_reservation",
                   "Create a Reservation" : "create_reservation",
                   "Lookup Flight Status" : "lookup_status",
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
        self.backButton.toggleActivation()

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
        pass

    def inflate(self):
        for i in self.attr:
            if type(i) == Button:
                i.toggleActivation()
            else:
                i.draw(self.win)
        return self.attr

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
