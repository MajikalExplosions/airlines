# Name: Actions.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0       Joseph Liu              05/27/20		Move actions and utils out of main and into a separate file
# 1.1       Chris Luey              05/27/20		Bug fixes (GUI display not working)


from random import randint


# Don't delete these.  I get errors when you do.

class ActionManager:
    def __init__(self, fs, gui, rm):
        self.fs = fs
        self.gui = gui
        self.rm = rm
        self._tripType = 1
        self._selectMode = 0
        self._airportLists = [[], []]
        self._paths = []
        self._start, self._end = 0, 0
        self._flightInfo = {}

    def runFlightStatusLookup(self):
        # TODO fix this up after Considine replies.
        dest = self.gui.findWidgetByID("flight_status: flight_destination").getText()
        num = self.gui.findWidgetByID("flight_status: flight_number").getText()
        status = self.gui.findWidgetByID("flight_status: status")
        time = self.gui.findWidgetByID("flight_status: time")

        try:
            if len(dest) == 0 or len(num) == 0:
                time.setText("Your input is empty.")
            elif type(int(num[2:])) == int and len(dest) == 3 and self.fs.isValidAirport(dest):
                flight = self.fs.searchForFlight(dest, num)
                if type(flight) == str:
                    time.setText(flight)
                else:
                    if not (dest + num) in self._flightInfo.keys():
                        x = randint(0, 2)
                        self._flightInfo[dest + num] = ("Status: {}".format(["On Time", "Delayed", "Cancelled"][x]),
                                                        "Flight Number {} to {}\n{}".format(num, dest,
                                                                                            ["", str(randint(20,
                                                                                                             120)) + " minutes",
                                                                                             ""][x]))
                    status.setText(self._flightInfo[dest + num][0])
                    time.setText(self._flightInfo[dest + num][1])
            else:
                status.setText("Error")
                time.setText("Destination '{}' is not Valid".format(num, dest))

        except ValueError:
            status.setText("Error")
            if not self.fs.isValidAirport(dest):
                time.setText("Flight Number '{}'\nand Destination '{}' is Not Valid".format(num, dest))
            else:
                time.setText("Flight Number '{}' is Not Valid".format(num))

        except IndexError:
            status.setText("Error")
            if not self.fs.isValidAirport(dest):
                time.setText("Flight Number '{}'\nand Destination '{}' is Not Valid".format(num, dest))
            else:
                time.setText("Flight Number '{}' is Not Valid".format(num))

    def runCreateReservationOneway(self):
        # Undraw prompt for return flight date
        if self._tripType != 0:
            self.gui.findWidgetByID("FlightReturnDateText").undraw()
            self.gui.findWidgetByID("create_reservation: return_date").undraw()

        # Move selection dot thing over
        self.gui.findWidgetByID("create_reservation: moving_circle").move(
            370 - self.gui.findWidgetByID("create_reservation: moving_circle").getCenter().getX(),
            475 - self.gui.findWidgetByID("create_reservation: moving_circle").getCenter().getY())

        self._tripType = 0

    def runCreateReservationRoundtrip(self):
        # Draw prompt for return flight date
        if self._tripType != 1:
            try:
                self.gui.findWidgetByID("FlightReturnDateText").draw(self.gui.getWin())
                self.gui.findWidgetByID("create_reservation: return_date").draw(self.gui.getWin())
            except:
                pass

        # Move selection dot thing over if necessary
        self.gui.findWidgetByID("create_reservation: moving_circle").move(
            135 - self.gui.findWidgetByID("create_reservation: moving_circle").getCenter().getX(),
            475 - self.gui.findWidgetByID("create_reservation: moving_circle").getCenter().getY())

        self._tripType = 1

    def runCreateReservationSearchFlights(self):
        # TODO Check date, traveler and airport inputs
        if self._start == 0 or self._end == 0:
            print("Invalid start or end airports.")
            return
        # TODO Check if self._start == the Entry, otherwise user has changed entry without selecting airport
        self.gui.switchScreen("list_flights")
        for k in range(10):
            self._paths = self.fs.searchForFlights(self._start, self._end, k, 2020, 5, 27)
            try:
                self.gui.findWidgetByID("selection_flight" + str(k)).setText(self._flights[k].toShortString(self.fm))
            except:
                self.gui.findWidgetByID("selection_circle_flight" + str(k)).undraw()
                self.gui.findWidgetByID("selection_flight" + str(k)).toggleActivation()
                self.gui.findWidgetByID("selection_flight" + str(k)).undraw()

    def runCreateReservationSearchAirports(self, mode):
        # Get the query
        self._selectMode = mode
        modes = ["start", "destination"]
        query = self.gui.findWidgetByID("create_reservation: " + modes[mode]).getText()
        # Search for query
        if query:
            self._airportLists[mode] = self.fs.searchForAirports(query)
            if self._airportLists[mode]:
                self.gui.switchScreen("list_airports")

                # Try to draw the queries, if the returned list is less than 10 long it will undraw the rest.
                for i in range(10):
                    try:
                        self.gui.findWidgetByID("selection_airport" + str(i)).setText(
                            self._airportLists[mode][i].toString())
                        # self.gui.findWidgetByID("selection_circle" + str(i)).draw(self.gui.getWin())
                    except:
                        self.gui.findWidgetByID("selection_circle" + str(i)).undraw()
                        self.gui.findWidgetByID("selection_airport" + str(i)).toggleActivation()
                        self.gui.findWidgetByID("selection_airport" + str(i)).undraw()

    def runCreateReservationSelectAirport(self, i):
        # Update text
        print("Selected airport.")
        if self._selectMode == 1:
            self.gui.findWidgetByID("create_reservation: destination").setText(self._airportLists[1][i].getCode())
            self._end = self._airportLists[1][i]
        else:
            self.gui.findWidgetByID("create_reservation: start").setText(self._airportLists[0][i].getCode())
            self._start = self._airportLists[0][i]

        # Switch screen back
        self.gui.switchScreen("create_reservation")

    def runCreateReservationSelectFlight(self, i):
        print("Selected flight.")
        path = self._paths[i]
        for flight in path.toFlights(self.fm):
            pass

        # TODO Create a reservation
        # TODO Switch screen to passenger information

    def runModifyReservationFindExisting(self):
        print("Finding existing reservation.")

        # TODO update the following section once Shuvam finishes ReservationManager and Chris finishes GUI
        cn, ln = self.gui.findWidgetByID("modify_reservation: reservation_number").getText(), self.gui.findWidgetByID(
            "modify_reservation: last_name").getText()
        reservation = self.rm.loadReservation(cn, ln)
        if reservation != 0:
            pass
