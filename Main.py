# Name: Main.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0       Christopher Luey        05/17/20		Original
# 1.1       Christopher Luey        05/17/20		Compatibility with widget id system
# 1.2       Christopher Luey        05/27/20		Complete Lookup flight
# 1.3       Christopher Luey        05/27/20		Complete Reservation


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


def searchAirport(gui, fs, t):
    query = gui.findWidgetByID("create_reservation: " + t).getText()
    if query:
        r = fs.searchForAirports(query)
        if r:
            gui.switchScreen("list_airports")
            for i in range(10):
                try:
                    gui.findWidgetByID("selection_airport" + str(i)).setText(r[i].toString())
                except:
                    gui.findWidgetByID("selection_circle" + str(i)).undraw()
                    gui.findWidgetByID("selection_airport" + str(i)).toggleActivation()
                    gui.findWidgetByID("selection_airport" + str(i)).undraw()
            return r


def main():
    fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    fs = FlightSearcher(fm)
    gui = GUI()
    clicked = 0
    screens = gui.getScreenIDs()
    cache = {}
    trip = "round"
    selecting = "start"
    start, destination = None, None

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
                    475 - gui.findWidgetByID("create_reservation: moving_circle").getCenter().getY())
                try:
                    gui.findWidgetByID("FlightReturnDateText").undraw()
                    gui.findWidgetByID("create_reservation: return_date").undraw()
                except:
                    pass
            elif clicked == "create_reservation: round-trip":
                trip = "round"
                gui.findWidgetByID("create_reservation: moving_circle").move(
                    135 - gui.findWidgetByID("create_reservation: moving_circle").getCenter().getX(),
                    475 - gui.findWidgetByID("create_reservation: moving_circle").getCenter().getY())
                try:
                    gui.findWidgetByID("FlightReturnDateText").draw(gui.getWin())
                    gui.findWidgetByID("create_reservation: return_date").draw(gui.getWin())
                except:
                    pass
            elif clicked == "create_reservation: find_flights":

                # TODO Check date, traveler and airport inputs

                gui.switchScreen("list_flights")
                s, dest, flights = start, destination, []
                for k in range(10):
                    flights = fs.searchForFlights(start, destination, k)
                for i in range(10):
                    try:
                        # TODO Can Someone Format The Paths Cuz I Dont Really Know & IHave Other Work
                        gui.findWidgetByID("selection_flight" + str(i)).setText(flights[i].toString(fm))
                    except:
                        gui.findWidgetByID("selection_circle_flight" + str(i)).undraw()
                        gui.findWidgetByID("selection_flight" + str(i)).toggleActivation()
                        gui.findWidgetByID("selection_flight" + str(i)).undraw()

            elif clicked == "create_reservation: find_start_airport":
                selecting = "start"
                startSelect = searchAirport(gui, fs, "start")

            elif clicked == "create_reservation: find_destination_airport":
                selecting = "destination"
                destSelect = searchAirport(gui, fs, "destination")

            elif clicked.find("selection_airport") != -1:
                if selecting == "destination":
                    gui.findWidgetByID("create_reservation: destination").setText(
                        destSelect[int(clicked[-1])].getCode())
                    destination = destSelect[int(clicked[-1])]
                    gui.switchScreen("create_reservation")
                else:
                    gui.findWidgetByID("create_reservation: start").setText(startSelect[int(clicked[-1])].getCode())
                    gui.switchScreen("create_reservation")
                    start = startSelect[int(clicked[-1])]

            elif clicked.find("selection_flight") != -1:
                pass
                # TODO Create a reservation
                # TODO Switch screen to passenger information



def lookup(gui, fs, cache):
    dest = gui.findWidgetByID("flight_status: flight_destination").getText()
    num = gui.findWidgetByID("flight_status: flight_number").getText()
    status = gui.findWidgetByID("flight_status: status")
    time = gui.findWidgetByID("flight_status: time")
    try:
        if len(dest) == 0 or len(num) == 0:
            time.setText("Your input is empty.")
        elif type(int(num[2:])) == int and len(dest) == 3 and fs.isValidAirport(dest):
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
                for airport in fs.searchForFlights(fs.searchForAirports(t[2])[0], fs.searchForAirports(t[3])[0], int(t[4]))[0].toFlights(fm):
                    print(airport.toString())


if __name__ == '__main__':
    main()
    #test()


