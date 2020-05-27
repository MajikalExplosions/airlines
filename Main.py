# Name: Main.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0       Christopher Luey        05/17/20		Original
# 1.1       Christopher Luey        05/17/20		Compatibility with widget id system
# 1.2       Christopher Luey        05/27/20		Lookup flight

from random import randint

from UI.GUI import GUI
from flights.FlightSearcher import *


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
    # fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    # fs = FlightSearcher(fm)
    fs, fm = None, None
    gui = GUI()
    clicked = 0
    screens = gui.getScreenIDs()
    cache = {}
    trip = "round"

    while clicked != 'quit':
        checkForDraw(gui, trip)
        clicked = gui.setOnButtonClickListener()
        if clicked == 'quit':
            break
        print("ID:", clicked, "- Action Performed")
        if clicked in screens or clicked == 'back':
            if clicked == 'back':
                gui.resetScreen(gui.getScreenID(gui.getScreen()))
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


def lookup(gui, fs, cache):
    dest = gui.findWidgetByID("flight_status: flight_destination").getText()
    num = gui.findWidgetByID("flight_status: flight_number").getText()
    status = gui.findWidgetByID("flight_status: status")
    time = gui.findWidgetByID("flight_status: time")
    try:
        if len(dest) == 0 or len(num) == 0:
            time.setText("Your input is empty.")
        elif type(int(num)) == int and len(dest) == 3 and fs.isValidAirport(dest):
            flight = fs.lookup(dest, num)
            if type(flight) == str:
                time.setText(flight)
            else:
                if not (dest + num) in cache.keys():
                    x = randint(0, 2)
                    cache[dest + num] = ("Status: {}".format(["On Time", "Delayed", "Cancelled"][x]),
                                         "Flight Number {} to {}\n{}".format(num, dest,
                                                                             ["", str(randint(20, 120)) + " minutes",
                                                                              ""][x]))
                status.setText(cache[dest + num][0])
                time.setText(cache[dest + num][1])
        else:
            status.setText("Error")
            time.setText("Destination '{}' is not Valid".format(num, dest))

    except ValueError:
        status.setText("Error")
        if not fs.isValidAirport(dest):
            time.setText("Flight Number '{}'\nand Destination '{}' is Not Valid".format(num, dest))
        else:
            time.setText("Flight Number '{}' is Not Valid".format(num))


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
                for airport in fs.searchForFlights(fs.searchForAirports(t[2])[0], fs.searchForAirports(t[3])[0], int(t[4]), fm)[0].toFlights(fm):
                    print(airport.toString())


if __name__ == '__main__':
    #main()
    test()


