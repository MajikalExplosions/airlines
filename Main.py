# Name: Main.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0       Christopher Luey        05/17/20		Original
# 1.1       Christopher Luey        05/17/20		Compatibility with widget id system
# 1.2       Christopher Luey        05/27/20		Complete Lookup flight
# 1.3       Christopher Luey        05/27/20		Complete Reservation
# 2.0       Joseph Liu              05/27/20        Move helper functions into Actions.py


from random import randint

from UI.GUI import GUI
from flights.FlightSearcher import FlightSearcher
from flights.FlightManager import FlightManager
from reservations.ReservationManager import ReservationManager
from Actions import ActionManager

def main():
    fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    fs = FlightSearcher(fm)
    gui = GUI()
    rm = ReservationManager()
    rm.loadAllReservations()
    
    am = ActionManager(fs, gui, rm)
    clicked = ""

    while clicked != 'quit':
        clicked = gui.setOnButtonClickListener()

        if clicked == 'quit':
            break

        print("ID:", clicked, "- Action Performed")
        if clicked in gui.getScreenIDs() or clicked == 'back':
            #Reset dot to original location
            if clicked == "create_reservation":
                am.runCreateReservationRoundtrip()
            
            if clicked == 'back':
                gui.resetScreen(gui.getScreenID(gui.getScreen()))
            
            gui.switchScreen(clicked)
        
        if clicked == "flight_status: lookup":
            am.runFlightStatusLookup()
        
        if clicked == "create_reservation: oneway-trip":
            am.runCreateReservationOneway()

        if clicked == "create_reservation: round-trip":
            am.runCreateReservationRoundtrip()
        
        if clicked == "create_reservation: find_flights":
            am.runCreateReservationSearchFlights()
        
        if clicked == "create_reservation: find_start_airport":
            am.runCreateReservationSearchAirports(0)
        
        if clicked == "create_reservation: find_destination_airport":
            am.runCreateReservationSearchAirports(1)
        
        if clicked == "modify_reservation: find_reservation":
            am.runCreateReservationSearchAirports(1)

        if clicked.find("selection_airport") != -1:
            am.runCreateReservationSelectAirport(int(clicked[-1]))
        
        if clicked.find("selection_flight") != -1:
            am.runCreateReservationSelectFlight(int(clicked[-1]))


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


