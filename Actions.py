# Name: Actions.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0       Joseph Liu              05/27/20		Move actions and utils out of main and into a separate file
# 1.1       Chris Luey              05/27/20		Bug fixes (GUI display not working) & back button fix, refactor


from random import randint

from reservations.BoardingPass import BoardingPass
from reservations.Passenger import Passenger
from flights.Time import *

class ActionManager:
    def __init__(self, fm, fs, gui, rm):
        self.fm = fm
        self.fs = fs
        self.gui = gui
        self.rm = rm
        self._tripType = 1
        self._airportSelectMode = 0
        self._airportLists = [[], []]
        self._paths = []
        self._start, self._end = 0, 0
        self._flightInfo = {}
        self._passengerCount = 0
        self._passengers = []
        self._startDate, self._returnDate = t_starttime, t_starttime
        self._flightSeatingIndex, self._passengerSeatingIndex = 0, 0
        self._seatSelectionMode = 0
        self._currentReservation = ""
        self._selectedPaths = [0, 0]
        self._selectFlightMode = 0
        self.k = 2

    def runFlightStatusLookup(self):
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
            self.gui.findWidgetByID("FlightReturnDateText").draw(self.gui.getWin())
            self.gui.findWidgetByID("create_reservation: return_date").draw(self.gui.getWin())

        # Move selection dot thing over if necessary
        self.gui.findWidgetByID("create_reservation: moving_circle").move(
            135 - self.gui.findWidgetByID("create_reservation: moving_circle").getCenter().getX(),
            475 - self.gui.findWidgetByID("create_reservation: moving_circle").getCenter().getY())

        self._tripType = 1

    def runCreateReservationSearchFlights(self):
        count, startD = self.gui.findWidgetByID("create_reservation: travelers").getText(), self.gui.findWidgetByID("create_reservation: start_date").getText()
        if self._tripType == 1:
            endD = self.gui.findWidgetByID("create_reservation: return_date").getText()
        if self._start == 0 or self._end == 0 or self._start == self._end:
            print("Invalid start or end airports.")
            return

        try:
            count = int(count)
            if count <= 0:
                print("You need to have at least 1 passenger.")
                return
            self._passengerCount = count
            self._passengers = []

            startD = startD.split("/")
            if self._tripType == 1:
                endD = endD.split("/")
            if len(startD) != 3:
                print("Start date is invalid")
                return

            if self._tripType == 1 and len(endD) != 3:
                print("End date is invalid.")
                return

            self._startDate = datetime(year=int(startD[2]), month=int(startD[0]), day=int(startD[1]))
            setStartDate(self._startDate.year, self._startDate.month, self._startDate.day)
            if self._tripType == 1:
                self._endDate = datetime(year=int(endD[2]), month=int(endD[0]), day=int(endD[1]))
        except ValueError:
            print("Input is invalid")
            return

        for k in range(self.k):
            print("Finding path", k)
            self._paths = self.fs.searchForFlights(self._start, self._end, k + 1, self._startDate.year, self._startDate.month, self._startDate.day)
            if k == 0:
                if not self._paths:
                    break
                else:
                    self.gui.switchScreen("list_flights")
            try:
                self.gui.findWidgetByID("selection_flight" + str(k)).setText(self._paths[k].toShortString(self.fm))
            except:
                self.gui.findWidgetByID("selection_circle_flight" + str(k)).undraw()
                self.gui.findWidgetByID("selection_flight" + str(k)).toggleActivation()
                self.gui.findWidgetByID("selection_flight" + str(k)).undraw()

    def runCreateReservationSearchAirports(self, mode):
        # Get the query
        self._airportSelectMode = mode
        modes = ["start", "destination"]
        query = self.gui.findWidgetByID("create_reservation: " + modes[mode]).getText()
        # Search for query
        if query:
            self._airportLists[mode] = self.fs.searchForAirports(query)
            if self._airportLists[mode]:
                self.gui.switchScreen("list_airports")

                # Try to draw the queries, if the returned list is less than self.k long it will undraw the rest.
                for i in range(self.k):
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
        if self._airportSelectMode == 1:
            self.gui.findWidgetByID("create_reservation: destination").setText(self._airportLists[1][i].getCode())
            self._end = self._airportLists[1][i]
        else:
            self.gui.findWidgetByID("create_reservation: start").setText(self._airportLists[0][i].getCode())
            self._start = self._airportLists[0][i]

        # Switch screen back
        self.gui.switchScreen("create_reservation")

    def runCreateReservationSelectFlight(self, i):
        self._selectedPaths[self._selectFlightMode] = self._paths[i]
        if self._tripType == 1:
            self._selectFlightMode = (self._selectFlightMode + 1) % 2
        self.gui.switchScreen("select_passenger")
        
    def runCheckinFindReservation(self):
        cn, ln = self.gui.findWidgetByID("checkin: reservation_number").getText(), self.gui.findWidgetByID("checkin: last_name").getText()
        try:
            reservation = self.rm.loadReservation(cn, ln)
            boardingPass = BoardingPass(reservation)
            display = "Boarding pass exported to " + boardingPass.export()
        except:
            display = "Reservation not found. Please try again."

        # TODO update display with message somewhere

    def runSelectPassengerNext(self):
        f, l = self.gui.findWidgetByID("select_passenger: first_name").getText(), self.gui.findWidgetByID(
            "select_passenger: last_name").getText()
        if len(f) == 0 or len(l) == 0:
            return

        self._passengers.append(Passenger(f, l))
        if len(self._passengers) == self._passengerCount:
            print("Complete")
            self.gui.switchScreen("select_seating")
            self._flightSeatingIndex, self._passengerSeatingIndex = 0, 0
            self._seatSelectionMode = 0
            
            self.gui.findWidgetByID("select_seat: text").setText(
                "Choose " + self._passengers[0].getFirstName() + " " + self._passengers[
                    0].getLastName() + "'s seat on " + self._selectedPaths[0].toFlights(self.fm)[0].getFullNumber())
        else:
            self.gui.findWidgetByID("select_passenger: first_name").setText("")
            self.gui.findWidgetByID("select_passenger: last_name").setText("")
    
    def runCreateReservationSelectSeats(self, row, seat, passengerIndex):
        self._passengers[passengerIndex].addSeat(str(row + 1) + ["A", "B", "C", "D", "E", "F"][seat])


    def runSelectSeats(self, i):
        if i[0] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            i = i[1:]
        
        row, seat = int(i[:-1]), int(i[-1])
        if self._seatSelectionMode == 0:

            self.runCreateReservationSelectSeats(row, seat, self._passengerSeatingIndex)
            self._passengerSeatingIndex += 1
            if self._passengerSeatingIndex >= self._passengerCount:
                self._passengerSeatingIndex -= self._passengerCount
                self._flightSeatingIndex += 1
                if (self._flightSeatingIndex == len(self._selectedPaths[0].toFlights(self.fm)) and self._tripType == 0) or (self._tripType == 1 and self._flightSeatingIndex == len(self._selectedPaths[0].toFlights(self.fm)) + len(self._selectedPaths[1].toFlights(self.fm))):
                    #Finish selecting seats so move on to credit card
                    self.gui.switchScreen("credit_card")
                    return
                
            self.gui.findWidgetByID("select_seat: text").setText("Choose " + self._passengers[self._passengerSeatingIndex].getFirstName() + " " + self._passengers[self._passengerSeatingIndex].getLastName() + "'s seat on " + self._selectedPaths[0].toFlights(self.fm)[self._flightSeatingIndex].getFullNumber())
        
        elif self._seatSelectionMode == 1:
            self.runModifyReservationSelectSeats(row, seat, self._passengers[self._passengerSeatingIndex])
            self._passengerSeatingIndex += 1
            if self._passengerSeatingIndex == len(self._passengers):
                self.gui.switchScreen("main")
    
    #self._seatSelectionMode = 1 somewhere at the end
    def runModifyReservationFindExisting(self):
        print("Finding existing reservation.")

        # TODO update the following section once Shuvam finishes ReservationManager and Chris finishes GUI
        cn, ln = self.gui.findWidgetByID("modify_reservation: reservation_number").getText(), self.gui.findWidgetByID(
            "modify_reservation: last_name").getText()
        reservation = self.rm.loadReservation(cn, ln)
        if reservation != 0:
            self.gui.findWidgetByID("modify_reservation_dates: start_date").setText(
                reservation.getFlights()[0].getDepDate())
            self._currentReservation = reservation

    def runModifyReservationChangeDate(self):
        # This is run after they enter a new date and submit it
        # self._seatSelectionMode = 1

        startdate = self.gui.findWidgetByID("modify_reservation_dates: start_date").getText()
        try:
            startdate = startdate.split("/")

            if len(startdate) != 3:
                print("Start date is invalid")
                return

            if self._currentReservation.getFlights()[0].getDepDate() != datetime(year=int(startdate[2]),
                                                                                 month=int(startdate[0]),
                                                                                 day=int(startdate[1])):
                self._seatSelectionMode = 1

                totalFlightTime = 0
                setStartDate(int(startdate[2]), int(startdate[0]), int(startdate[1]))

                for i in range(len(self._currentReservation.getFlights())):
                    nextFlightTime = self._currentReservation.getFlights()[i].timeUntilNextFlight(offsetStartTime(timedelta(hours=totalFlightTime)))
                    flightTime = self._currentReservation.getFlights()[i].getTravelTime()
                    totalFlightTime += nextFlightTime + flightTime
                
                #totalflighttime is in hours since starttime
                # TODO Allow user to select new flight
                # setStartDate()
                # TODO create new reservation set it to _currentReservation, update reservation manager

                pass

        except ValueError:
            print("Input is invalid")

    def runCreditCardCreateReservation(self):
        print("Created reservation")
        self.gui.switchScreen("create_reservation_success")
    
    def runCreateReservationSuccess(self):
        self.gui.switchScreen("main")

    def runModifyReservationSelectSeats(self, row, seat, passenger):
        #This is run after a seat is selected for modify reservation.
        self._currentReservation.modifySeat(row,seat,passenger.getFirstName(),passenger.getLastName(),self._flightSeatingIndex)
