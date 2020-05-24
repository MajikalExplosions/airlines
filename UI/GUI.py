# Name: UI.py
# Description: File for UI and screens

# Ver.	       Writer			 Date			Notes
# 1.0     Christopher Luey     05/08/20		    Master
# 1.1     Christopher Luey     05/15/20	        Add switchScreen method
# 1.2     Christopher Luey     05/15/20	        Add parsing method
# 1.3     Christopher Luey     05/23/20         Add widget id system & minor bug fixes


from UI.lib.Button import *


class GUI:

    def __init__(self):
        self.win = GraphWin(title="Airport", width=1200, height=800, autoflush=False)
        self.id_widget, self.widget_id = {}, {}
        ids = ['main', 'start', 'create_reservation', 'modify_reservation', 'flight_status', 'checkin']
        # self.screens - Hash: screenID : Screen()
        self.screens = {x:y for x,y in zip(ids, [Screen(i, self.win) for i in ids])}

        for i in self.screens.values():
            self.id_widget.update({x[1]:x[0] for x in i.getAttr()})
            self.widget_id.update({x[0]:x[1] for x in i.getAttr()})

        self.previousScreen = self.screens['main']
        self.inflate_header()
        self.activeScreen = self.screens['main']
        self.attrs = self.activeScreen.inflate()
        self.win.setBackground(color_rgb(self.activeScreen.getBackground()[0], self.activeScreen.getBackground()[1], self.activeScreen.getBackground()[2]))

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
            self.activeScreen = self.screens['main']
            self.attrs = self.activeScreen.inflate()
        elif screen == "create_reservation":
            self._switchScreen(self.screens['create_reservation'])
        elif screen == "modify_reservation":
            self._switchScreen(self.screens['modify_reservation'])
        elif screen == "flight_status":
            self._switchScreen(self.screens['flight_status'])
        elif screen == "checkin":
            self._switchScreen(self.screens['checkin'])
        elif screen == "start":
            self._switchScreen(self.screens['start'])
        elif screen == "back":
            if self.previousScreen == self.screens['main'] and self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.previousScreen, self.activeScreen = self.activeScreen, self.previousScreen
            self.attrs = self.activeScreen.inflate()
        else:
            raise("Could not locate screen")

        print("ID:", screen, "- Switch to Screen")

    def getScreen(self):
        return self.activeScreen

    def findWidgetByID(self, id):
        return self.id_widget[id]

    def findIDByWidget(self, wid):
        return self.widget_id[wid]

    def getWidgetIDs(self):
        return self.widget_id

    def getScreenIDs(self):
        return self.screens


    def _switchScreen(self, screen):
        if not self.backButton.isActive(): self.backButton.toggleActivation()
        self.activeScreen.deflate()
        self.previousScreen = self.activeScreen
        self.activeScreen = screen
        self.attrs = self.activeScreen.inflate()


    def setOnButtonClickListener(self):
        p = self.win.getMouse()
        while not self.quitButton.isClicked(p):
            for widget, id in self.widget_id.items():
                if type(widget) == Button and widget.isClicked(p):
                    return id
            if self.backButton.isClicked(p):
                return 'back'
            p = self.win.getMouse()
        return 'quit'


    def inflate_header(self):
        self.home = Button(595, 75/2 - 5, 1205, 80, 0, color_rgb(8, 76, 97), 'ᴀɪʀᴘᴏʀᴛ ᴘʀᴏɢʀᴀᴍ', 'white', 26, self.win)
        self.home.setInactiveColor(color_rgb(8, 76, 97))
        self.home.toggleActivation()
        self.home.toggleActivation()
        self.quitButton = Button(1125, 75 / 2, 100, 50, 5, color_rgb(219, 80, 74), "Exit", 'white', 20, self.win).toggleActivation()
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
        # self.ids = ids
        path = "UI/screens/" + name + ".txt"
        try:
            self.source_file = open(path, 'r')
            self.attr = self._parse(self.source_file)
        except:
            raise("Could not locate file: " + path)

    def deflate(self):
        for i in self.attr:
            if type(i[0]) == Button:
                i[0].toggleActivation()
            i[0].undraw()

    def inflate(self):
        for i in self.attr:
            if type(i[0]) == Button:
                if not i[0].isDrawn():
                    i[0].draw(self.win)
                if not i[0].isActive():
                    i[0].toggleActivation()
            else:
                i[0].draw(self.win)
        return self.attr

    def getName(self):
        return self.name

    def getAttr(self):
        return self.attr

    def _parse(self, s):

        """
        Args:
            s:
        """
        attrs = []

        source = s.readlines()
        if source:
            self.background = source[0].lstrip("Background: ").strip().split(",")
            for i in self.background:
                self.background[self.background.index(i)] = int(self.background[self.background.index(i)])
            i=2
            while i < len(source):
                if source[i][0] == "<" and source[i].lstrip("<").rstrip(">\n") == "Button":
                    attrs.append([Button(float(source[i+1].lstrip("x: ").rstrip("\n")), float(source[i+2].lstrip("y: ").rstrip("\n")), float(source[i+3].lstrip("width: ").rstrip("\n")), float(source[i+4].lstrip("height: ").rstrip("\n")), float(source[i+5].lstrip("radius: ").rstrip("\n")), color_rgb(int(source[i+6].lstrip("color: ").rstrip("\n").strip().split(",")[0]), int(source[i+6].lstrip("color: ").rstrip("\n").strip().split(",")[1]), int(source[i+6].lstrip("color: ").rstrip("\n").strip().split(",")[2])), str(source[i+7].lstrip("text: ").rstrip("\n")), color_rgb(int(source[i+8].lstrip("textColor: ").rstrip("\n").strip().split(",")[0]), int(source[i+8].lstrip("textColor: ").rstrip("\n").strip().split(",")[1]), int(source[i+8].lstrip("textColor: ").rstrip("\n").strip().split(",")[2])), int(source[i+9].lstrip("textSize: ").rstrip("\n")), self.win), source[i+10].lstrip("id: ").rstrip("\n")])
                    attrs[len(attrs)-1][0].undraw()
                    i+=13
                # elif source[i].rstrip("<").lstrip(">\n") == "Input":
                #     attrs.append()
                #     i = Entry(Point, width)
                #     i.
        return attrs


    def getBackground(self):
        return self.background[0], self.background[1], self.background[2]
