# Name: Main.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0       Christopher Luey        05/17/20		Original
# 1.1       Christopher Luey        05/17/20		Compatibility with widget id system


from UI.GUI import GUI
from flights.FlightSearcher import FlightSearcher
from flights.FlightManager import FlightManager
from reservations.ReservationManager import ReservationManager
from Actions import *


def checkForDraw(gui, trip):
    if gui.getScreen().getName() == "create_reservation":
        if trip == "round":
            try:
                gui.findWidgetByID("FlightReturnDateText").draw(gui.getWin())
                gui.findWidgetByID("create_reservation: return_date").draw(gui.getWin())
            except:
                pass
        else:
            try:
                gui.findWidgetByID("FlightReturnDateText").undraw()
                gui.findWidgetByID("create_reservation: return_date").undraw()
            except:
                pass


def main():
    fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    fs = FlightSearcher(fm)
    rm = ReservationManager()
    gui = GUI()
    manager = ActionManager(fs, rm, gui)
    clicked = ""
    screens = gui.getScreenIDs()
    while clicked != 'quit':
        screen = gui.getScreen()
        clicked = gui.setOnButtonClickListener()
        if clicked == 'quit':
            break
        print("ID:", clicked, "- Action Performed")
        if clicked in screens or clicked == 'back':
            gui.switchScreen(clicked)
        else:
            if clicked == "flight_status: lookup":
                lookup(gui, fs, cache)
            elif clicked == "create_reservation: oneway-trip":
                trip = "one"
                gui.findWidgetByID("create_reservation: moving_circle").move(
                    370 - gui.findWidgetByID("create_reservation: moving_circle").getCenter().getX(),
                    425 - gui.findWidgetByID("create_reservation: moving_circle").getCenter().getY())
                try:
                    gui.findWidgetByID("FlightReturnDateText").undraw()
                    gui.findWidgetByID("create_reservation: return_date").undraw()
                except:
                    pass
            elif clicked == "create_reservation: round-trip":
                trip = "round"
                gui.findWidgetByID("create_reservation: moving_circle").move(
                    135 - gui.findWidgetByID("create_reservation: moving_circle").getCenter().getX(),
                    425 - gui.findWidgetByID("create_reservation: moving_circle").getCenter().getY())
                try:
                    gui.findWidgetByID("FlightReturnDateText").draw(gui.getWin())
                    gui.findWidgetByID("create_reservation: return_date").draw(gui.getWin())
                except:
                    pass
            elif clicked == "create_reservation: find_flights":
                gui.switchScreen("list_flights")


def test():
    fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    fs = FlightSearcher(fm)
    inp = ""
    while inp != "quit":
        inp = input(">>> ").lower()
        t = inp.split()
        print(t)
        if t[0] == "search":
            if t[1] == "airport":
                for airport in fs.searchForAirports(t[2]): #Returns 10 airports with char
                    print(airport.toString())
            elif t[1] == "flight":
                if len(t) == 4:
                    t.append(5)
                for airport in fs.searchForFlights(fs.searchForAirports(t[2])[0], fs.searchForAirports(t[3])[0], int(t[4]))[0].toFlights(fm):
                    print(airport.toString())


if __name__ == '__main__':
    main()
