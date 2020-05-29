# Name: Main.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0       Christopher Luey        05/17/20		Original
# 1.1       Christopher Luey        05/17/20		Compatibility with widget id system
# 1.2       Christopher Luey        05/17/20		Add screen switching, all GUI elements displayed
# 1.3       Christopher Luey        05/27/20		Complete Lookup flight functionality
# 1.4       Christopher Luey        05/27/20		Complete Create Reservation up to search for flights
# 2.0       Joseph Liu              05/27/20        Move helper functions into Actions.py


from Actions import ActionManager
from UI.GUI import GUI
from flights.FlightManager import FlightManager
from flights.FlightSearcher import FlightSearcher
from reservations.ReservationManager import ReservationManager


def main():
    fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    fs = FlightSearcher(fm)
    gui = GUI()
    rm = ReservationManager()
    
    am = ActionManager(fm, fs, gui, rm)
    clicked = ""

    while clicked != 'quit':
        clicked = gui.setOnButtonClickListener()

        if clicked == 'quit':
            break

        print("ID:", clicked, "- Action Performed")
        if clicked in gui.getScreenIDs() or clicked == 'back':
            if clicked == 'back':
                gui.resetScreen(gui.getScreenID(gui.getScreen()))
                am.runCreateReservationUpdatetrip()

            gui.switchScreen(clicked)

            # Reset dot to original location
            if clicked == "create_reservation":
                am.runCreateReservationRoundtrip()

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

        if clicked == "create_reservation_success: main":
            gui.switchScreen("main")

        if clicked == "modify_reservation: find_reservation":
            am.runModifyReservationFindExisting()

        if clicked == "modify_reservation_dates: confirm":
            am.runModifyReservationChangeDate()

        if clicked == "checkin: find_reservation":
            am.runCheckinFindReservation()

        if clicked == "checkin_bags: next":
            am.runCheckinBagsNext()

        if clicked == "select_passenger: next":
            am.runSelectPassengerNext()

        if clicked == "credit_card: create":
            am.runCreditCardCreateReservation()

        if clicked.find("selection_airport") != -1:
            am.runCreateReservationSelectAirport(int(clicked[-1]))

        if clicked.find("selection_flight") != -1:
            am.runCreateReservationSelectFlight(int(clicked[-1]))
        
        if clicked.find("selection_seat") != -1:
            am.runSelectSeats(clicked[-3:])
        
        rm.serializeAll()


if __name__ == '__main__':
    main()
