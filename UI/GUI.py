# Name: UI.py
# Description: File for UI

# Ver.	       Writer			 Date		Notes
# 1.0     Christopher Luey     05/08/20     Master
# 1.1     Christopher Luey     05/15/20     Add switchScreen method
# 1.2     Christopher Luey     05/15/20	    Add parsing method for legacy .txt
# 1.3     Christopher Luey     05/23/20     Add widget id system & minor bug fixes
# 1.4     Christopher Luey     05/23/20     Add json compatibility, remove .txt parsing
# 1.5     Christopher Luey     05/26/20     Begin integration
# 1.6     Christopher Luey     05/27/20     Back button saves state
# 1.7     Christopher Luey     05/27/20     Display airports and flights



import json

from UI.lib.Button import *


class GUI:

    def __init__(self):
        self.win = GraphWin(title="Airport", width=1200, height=800, autoflush=False)
        self.id_widget, self.widget_id = {}, {}

        ids = ["main", "list_flights", "create_reservation", "modify_reservation", "flight_status", "checkin",
               "list_airports"]
        # self.screens - Hash: screenID : Screen()
        self.id_screen = {x: y for x, y in zip(ids, [Screen(i, self.win) for i in ids])}
        self.screen_id = {y: x for x, y in self.id_screen.items()}

        for i in self.id_screen.values():
            self.id_widget.update({x[1]: x[0] for x in i.getAttr()})
            self.widget_id.update({x[0]: x[1] for x in i.getAttr()})

        self._inflate_header()
        self.activeScreen = self.id_screen["main"]
        self.screen, self.index = [], 0
        self.activeScreen.inflate()
        self.switchScreen("main")

    def switchScreen(self, screen):
        """
        Args:
            screen:
        """

        if screen == "main":
            if self.backButton.isActive():
                self.backButton.toggleActivation()
            self.activeScreen.deflate()
            self.index += 1
            self.screen.append(self.id_screen["main"])
            self.activeScreen = self.screen[self.index - 1]
            self.attrs = self.activeScreen.inflate()

        elif screen == "back":
            if self.screen[self.index - 1] == self.id_screen["main"] and self.backButton.isActive():
                self.backButton.toggleActivation()

            self.activeScreen.deflate()
            self.index -= 1
            # if self.activeScreen == self.screen[self.index]:
            #     self.screen.pop(self.index)
            #     self.index-=1
            self.screen.append(self.screen[self.index])
            self.activeScreen = self.screen[self.index]
            self.attrs = self.activeScreen.inflate()
        else:
            self._switchScreen(self.id_screen[screen])

        print("ID:", screen, "- Switch to Screen")

    def getScreen(self):
        return self.activeScreen

    def findWidgetByID(self, id):
        try:
            return self.id_widget[id]
        except:
            raise Exception("Invalid Widget ID")

    def findIDByWidget(self, wid):
        try:
            return self.widget_id[wid]
        except:
            raise Exception("Invalid Widget")

    def getWidgetIDs(self):
        return self.widget_id

    def getScreenID(self, screen):
        return self.screen_id[screen]

    def getScreenIDs(self):
        return self.id_screen

    def getWin(self):
        return self.win

    def _switchScreen(self, screen):
        if not self.backButton.isActive(): self.backButton.toggleActivation()
        self.activeScreen.deflate()

        if screen.getName() != "list_airports":

            self.screen.append(screen)
            try:
                if self.screen[-1] == self.screen[len(self.screen) - 2]:
                    self.screen.pop()
            except:
                pass
            self.index = len(self.screen) - 1
            self.activeScreen = self.screen[self.index]
        else:
            try:
                if self.screen[-1] == self.screen[len(self.screen) - 2]:
                    self.screen.pop()
            except:
                pass
            self.index = len(self.screen)
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

    def _inflate_header(self):
        self.home = Button(595, 75 / 2 - 5, 1205, 80, 0, color_rgb(8, 76, 97), "ᴀɪʀᴘᴏʀᴛ ᴘʀᴏɢʀᴀᴍ", "white", 26, self.win)
        self.home.setInactiveColor(color_rgb(8, 76, 97))
        self.home.toggleActivation()
        self.home.toggleActivation()
        self.quitButton = Button(1125, 75 / 2, 100, 50, 5, color_rgb(219, 80, 74), "Exit", "white", 20,
                                 self.win).toggleActivation()
        self.backButton = Button(75, 75 / 2, 100, 50, 5, color_rgb(219, 80, 74), "Back", "white", 20, self.win)

    def resetScreen(self, screen):
        if screen == "flight_status":
            self.findWidgetByID("flight_status: flight_destination").setText("")
            self.findWidgetByID("flight_status: flight_number").setText("")
            self.findWidgetByID("flight_status: status").setText("Status: Unavailable")
            self.findWidgetByID("flight_status: time").setText("")


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
                if i[0].isActive():
                    i[0].toggleActivation()
            try:
                i[0].undraw()
            except:
                pass

    def inflate(self):
        for i in self.attr:
            if type(i[0]) == Button:
                if not i[0].isDrawn():
                    i[0].draw(self.win)
                if not i[0].isActive():
                    i[0].toggleActivation()
            else:
                try:
                    i[0].draw(self.win)
                except:
                    pass
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
                attrs[len(attrs) - 1][0].setTextColor(
                    color_rgb(item["textColor"]["r"], item["textColor"]["g"], item["textColor"]["b"]))
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
                attrs.append([Rectangle(Point(item["x"], item["y"]), Point(item["x2"], item["y2"])), item["id"]])
                attrs[len(attrs) - 1][0].setFill(color_rgb(item["color"]["r"], item["color"]["g"], item["color"]["b"]))
                attrs[len(attrs) - 1][0].setOutline(
                    color_rgb(item["color"]["r"], item["color"]["g"], item["color"]["b"]))

            elif str(key).find("Circle") != -1:
                attrs.append([Circle(Point(item["x"], item["y"]), item["radius"]), item["id"]])
                attrs[len(attrs) - 1][0].setFill(color_rgb(item["fill"]["r"], item["fill"]["g"], item["fill"]["b"]))
                attrs[len(attrs) - 1][0].setOutline(
                    color_rgb(item["outline"]["r"], item["outline"]["g"], item["outline"]["b"]))
                attrs[len(attrs) - 1][0].setWidth(item["width"])
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
            elif str(key).find("NoShadow") != -1:
                attrs.append([Button(item["x"], item["y"], item["width"], item["height"], item["radius"],
                                     color_rgb(item["color"]["r"], item["color"]['g'], item["color"]['b']),
                                     item["text"],
                                     color_rgb(item["textColor"]['r'], item["textColor"]['g'], item["textColor"]['b']),
                                     item["textSize"], self.win), item["id"]])
                attrs[len(attrs) - 1][0].adjustShadowColor('white')
                attrs[len(attrs) - 1][0].undraw()

            elif str(key).find("List10") != -1:
                for i in range(10):
                    attrs.append(
                        [Button(600, i * 50 + 275, 1200, 50, 20, 'white', "", color_rgb(27, 73, 101), 25, self.win),
                         "selection_airport" + str(i)])
                    attrs[len(attrs) - 1][0].adjustShadowColor('white')
                    attrs[len(attrs) - 1][0].undraw()
                    attrs.append([Circle(Point(100, i * 50 + 275), 10), "selection_circle" + str(i)])
                    attrs[len(attrs) - 1][0].setFill(color_rgb(255, 255, 255))
                    attrs[len(attrs) - 1][0].setOutline(color_rgb(98, 182, 203))
                    attrs[len(attrs) - 1][0].setWidth(3)
            elif str(key).find("Flight10") != -1:
                for i in range(10):
                    attrs.append(
                        [Button(600, i * 50 + 275, 1200, 50, 20, 'white', "", color_rgb(27, 73, 101), 25, self.win),
                         "selection_flight" + str(i)])
                    attrs[len(attrs) - 1][0].adjustShadowColor('white')
                    attrs[len(attrs) - 1][0].undraw()
                    attrs.append([Circle(Point(100, i * 50 + 275), 10), "selection_circle_flight" + str(i)])
                    attrs[len(attrs) - 1][0].setFill(color_rgb(255, 255, 255))
                    attrs[len(attrs) - 1][0].setOutline(color_rgb(98, 182, 203))
                    attrs[len(attrs) - 1][0].setWidth(3)

        return attrs


class Gradient:
    def __init__(self):
        pass
