# Name: UI.py
# Description: File for UI

# Ver.	       Writer			 Date		Notes
# 1.0     Christopher Luey     05/08/20     Master
# 1.1     Christopher Luey     05/15/20     Add switchScreen method
# 1.2     Christopher Luey     05/15/20	    Add parsing method for legacy .txt
# 1.3     Christopher Luey     05/23/20     Add widget id system & minor bug fixes
# 1.4     Christopher Luey     05/23/20     Add json compatibility, remove .txt parsing
# 1.5     Christopher Luey     05/26/20     Begin integration


import json

from UI.lib.Button import *


class GUI:

    def __init__(self):
        self.win = GraphWin(title="Airport", width=1200, height=800, autoflush=False)
        self.id_widget, self.widget_id = {}, {}

        ids = ["main", "start", "create_reservation", "modify_reservation", "flight_status", "checkin"]
        # self.screens - Hash: screenID : Screen()
        self.screens = {x: y for x, y in zip(ids, [Screen(i, self.win) for i in ids])}

        for i in self.screens.values():
            self.id_widget.update({x[1]: x[0] for x in i.getAttr()})
            self.widget_id.update({x[0]: x[1] for x in i.getAttr()})

        print(self.id_widget)
        self.previousScreen = self.screens["main"]
        self.activeScreen = self.screens["main"]
        self.attrs = self.activeScreen.inflate()
        self.inflate_header()

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
            self.activeScreen = self.screens["main"]
            self.attrs = self.activeScreen.inflate()
        elif screen == "create_reservation":
            self._switchScreen(self.screens["create_reservation"])
        elif screen == "modify_reservation":
            self._switchScreen(self.screens["modify_reservation"])
        elif screen == "flight_status":
            self._switchScreen(self.screens["flight_status"])
        elif screen == "checkin":
            self._switchScreen(self.screens["checkin"])
        elif screen == "start":
            self._switchScreen(self.screens["start"])
        elif screen == "back":
            if self.previousScreen == self.screens["main"] and self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.previousScreen, self.activeScreen = self.activeScreen, self.previousScreen
            self.attrs = self.activeScreen.inflate()
        else:
            raise Exception("Could not locate screen")

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
                return "back"
            p = self.win.getMouse()
        self.win.close()
        return "quit"

    def inflate_header(self):
        self.home = Button(595, 75 / 2 - 5, 1205, 80, 0, color_rgb(8, 76, 97), "ᴀɪʀᴘᴏʀᴛ ᴘʀᴏɢʀᴀᴍ", "white", 26, self.win)
        self.home.setInactiveColor(color_rgb(8, 76, 97))
        self.home.toggleActivation()
        self.home.toggleActivation()
        self.quitButton = Button(1125, 75 / 2, 100, 50, 5, color_rgb(219, 80, 74), "Exit", "white", 20,
                                 self.win).toggleActivation()
        self.backButton = Button(75, 75 / 2, 100, 50, 5, color_rgb(219, 80, 74), "Back", "white", 20, self.win)


class Screen:

    def __init__(self, name, win):
        """
        Args:
            name:
            win:
        """
        self.name = name
        self.win = win
        path = "UI/Screens/" + name + ".json"
        try:
            self.source_file = open(path, "r")
            self.attr = self._parse(self.source_file)
        except:
            raise ("Could not locate file: " + path)

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

        d = json.load(s)
        for key, item in d.items():
            if str(key).find("Button") != -1:
                attrs.append([Button(item["x"], item["y"], item["width"], item["height"], item["radius"],
                                     color_rgb(item["color"]["r"], item["color"]['g'], item["color"]['b']),
                                     item["text"],
                                     color_rgb(item["textColor"]['r'], item["textColor"]['g'], item["textColor"]['b']),
                                     item["textSize"], self.win), item["id"]])
                attrs[len(attrs) - 1][0].undraw()
            elif str(key).find("Entry") != -1:
                attrs.append([Entry(Point(item["x"], item["y"]), item["width"]), item["id"]])
                attrs[len(attrs) - 1][0].setTextColor(color_rgb(item["textColor"]["r"], item["textColor"]["g"], item["textColor"]["b"]))
                attrs[len(attrs) - 1][0].setSize(item["size"])
                attrs[len(attrs) - 1][0].setText(item["text"])
                attrs[len(attrs) - 1][0].setFill(color_rgb(item["fill"]["r"], item["fill"]["g"], item["fill"]["b"]))
                attrs[len(attrs) - 1][0].setStyle(item["style"])
            elif str(key).find("Text") != -1:
                attrs.append([Text(Point(item["x"], item["y"]), item["text"]), item["id"]])
                attrs[len(attrs) - 1][0].setTextColor(
                    color_rgb(item["color"]["r"], item["color"]["g"], item["color"]["b"]))
                attrs[len(attrs) - 1][0].setStyle(item["style"])
                attrs[len(attrs) - 1][0].setSize(item["size"])
                pass
            elif str(key).find("Rectangle") != -1:
                pass
            elif str(key).find("Circle") != -1:
                attrs.append([Circle(Point(item["x"], item["y"]), item["radius"]), item["id"]])
                attrs[len(attrs) - 1][0].setFill(color_rgb(item["fill"]["r"], item["fill"]["g"], item["fill"]["b"]))
                attrs[len(attrs) - 1][0].setOutline(
                    color_rgb(item["outline"]["r"], item["outline"]["g"], item["outline"]["b"]))

            elif str(key).find("Point") != -1:
                pass
            elif str(key).find("Oval") != -1:
                pass
            elif str(key).find("Line") != -1:
                pass
            elif str(key).find("Polygon") != -1:
                pass
            elif str(key).find("Image") != -1:
                pass

        return attrs


class Gradient:
    def __init__(self):
        pass
