# Name: Actions.py
# Description: Utility class containing functions called by main

# Ver.	    Writer			        Date			Notes
# 1.0       Joseph Liu              05/27/20		Move actions and utils out of main and into a separate file
# 1.1       Chris Luey              05/27/20		Bug fixes (GUI display not working) & back button fix, refactor
# 1.2       Shuvam Chatterjee       05/28/20        Reservation creation functions
# 2.0       Everybody at once       05/28/20        Finish all missing functions


from random import randint

from flights.Airport import Airport
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
        self._currentTripSelect = 0
        self._airportSelectMode = 0
        self._airportLists = [[], []]
        self._paths = []
        self._start, self._end = 0, 0
        self._flightInfo = {}
        self._passengerCount = 0
        self._passengers, self._passengersAlt = [], []
        self._startDate, self._returnDate = t_starttime, t_starttime
        self._flightSeatingIndex, self._passengerSeatingIndex = 0, 0
        self._seatSelectionMode = 0
        self._currentReservation, self._currentReservationAlt = "", ""
        self._selectedPaths = [0, 0]
        self._selectFlightMode = 0
        self.k = 10
        self._checkinReservation, self._checkinCurrentPassenger = None, 0
        self.singleFlights, self.singleFlightsAlt = [], []


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
        try:
            self.gui.findWidgetByID("FlightReturnDateText").undraw()
            self.gui.findWidgetByID("create_reservation: return_date").undraw()
        except:
            pass

        # Move selection dot thing over
        self.gui.findWidgetByID("create_reservation: moving_circle").move(
            370 - self.gui.findWidgetByID("create_reservation: moving_circle").getCenter().getX(),
            475 - self.gui.findWidgetByID("create_reservation: moving_circle").getCenter().getY())

        self._tripType = 0

    def runCreateReservationRoundtrip(self):
        # Draw prompt for return flight date
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

    def runCreateReservationUpdatetrip(self):
        if self.gui.getScreen().getName() == "create_reservation":
            if self._tripType == 0:
                try:
                    self.gui.findWidgetByID("FlightReturnDateText").undraw()
                    self.gui.findWidgetByID("create_reservation: return_date").undraw()
                except:
                    pass
            else:
                try:
                    self.gui.findWidgetByID("FlightReturnDateText").draw(self.gui.getWin())
                    self.gui.findWidgetByID("create_reservation: return_date").draw(self.gui.getWin())
                except:
                    pass

    def runCreateReservationSearchFlights(self):
        # Error check user input
        count, startD = self.gui.findWidgetByID("create_reservation: travelers").getText(), self.gui.findWidgetByID(
            "create_reservation: start_date").getText()
        if self._tripType == 1:
            endD = self.gui.findWidgetByID("create_reservation: return_date").getText()
        if self._start == 0 or self._end == 0:
            self.gui.findWidgetByID("create_reservation: output").setText(
                "Invalid Airports.\nPlease press Find Start or Find Destination to select your airport.")
            return
        if self._start == self._end:
            self.gui.findWidgetByID("create_reservation: output").setText(
                "Invalid Airports.\nDeparture airport is the same as arrival airport.")
            return
        if self._start.getCode() != self.gui.findWidgetByID(
                "create_reservation: start").getText() or self._end.getCode() != self.gui.findWidgetByID(
            "create_reservation: destination").getText():
            self.gui.findWidgetByID("create_reservation: output").setText(
                "Changes to your input detected.\nPlease press Find Start or Find Destination to select the airport")
            return

        try:
            count = int(count)
            if count <= 0:
                self.gui.findWidgetByID("create_reservation: output").setText(
                    "You need to have at least 1 passenger")
                return
            self._passengerCount = count
            self._passengers = []

            startD = startD.split("/")
            if self._tripType == 1:
                endD = endD.split("/")
            if len(startD) != 3:
                self.gui.findWidgetByID("create_reservation: output").setText(
                    "Start date is invalid.")
                return

            if self._tripType == 1 and len(endD) != 3:
                self.gui.findWidgetByID("create_reservation: output").setText(
                    "Return date is invalid.")
                return

            self._startDate = datetime(year=int(startD[2]), month=int(startD[0]), day=int(startD[1]))

            setStartDate(self._startDate.year, self._startDate.month, self._startDate.day)
            if self._tripType == 1:
                self._endDate = datetime(year=int(endD[2]), month=int(endD[0]), day=int(endD[1]))
        except ValueError:
            self.gui.findWidgetByID("Invalid input for passengers. Must be a number.")
            return

        for k in range(self.k):
            print("Finding path", k)
            self.gui.findWidgetByID("create_reservation: output").setText(
                "Calculating Flight Paths...")
            self._paths = self.fs.searchForFlights(self._start, self._end, k + 1, self._startDate.year,
                                                   self._startDate.month, self._startDate.day)
            if k == 0:
                if not self._paths:
                    break
                else:
                    self.gui.switchScreen("list_flights")
                    self.gui.findWidgetByID("create_reservation: output").setText("")
            try:
                self.gui.findWidgetByID("selection_flight" + str(k)).setText(self._paths[k].toShortString(self.fm))
            except:
                self.gui.findWidgetByID("selection_circle_flight" + str(k)).undraw()
                self.gui.findWidgetByID("selection_flight" + str(k)).toggleActivation()
                self.gui.findWidgetByID("selection_flight" + str(k)).undraw()
        
    #This is called for the inbound flight
    def runCreateReservationSearchFlightsAlt(self):
        for k in range(self.k):
            print("Finding path", k)
            self._paths = self.fs.searchForFlights(self._end, self._start, k + 1, self._endDate.year, self._endDate.month, self._endDate.day)
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
        try:
            if self._tripType != 0:
                self.gui.findWidgetByID("FlightReturnDateText").draw(self.gui.getWin())
                self.gui.findWidgetByID("create_reservation: return_date").draw(self.gui.getWin())
            else:
                self.gui.findWidgetByID("FlightReturnDateText").undraw()
                self.gui.findWidgetByID("create_reservation: return_date").undraw()
        except:
            pass

    def runCreateReservationSelectFlight(self, i):
        self._selectedPaths[self._selectFlightMode] = self._paths[i]
        if self._tripType == 1:
            self._selectFlightMode = (self._selectFlightMode + 1) % 2
        if self._currentTripSelect == 0:
            self.gui.switchScreen("select_passenger")
            self.gui.findWidgetByID("select_passenger: output").setText(
                "Fill in first and last name for passenger " + str(len(self._passengers) + 1))

        elif self._currentTripSelect == 1:            
        
            if self._currentTripSelect == 1:
                for passenger in self._passengers:
                    self._passengersAlt.append(Passenger(passenger.getFirstName(), passenger.getLastName()))

                self.gui.switchScreen("select_seating")


                self._flightSeatingIndex, self._passengerSeatingIndex = 0, 0
                self._seatSelectionMode = 0
                
                #Gray out taken seats
                seatA = self.__getSeatAvailability(self._selectedPaths[self._currentTripSelect].toFlights(self.fm)[self._flightSeatingIndex], self._startDate, self._currentTripSelect == 0)
                for i in range(len(seatA)):
                    for j in range(len(seatA[i])):
                        if not seatA[i][j]:
                            self.gui.findWidgetByID("selection_seat" + str(i) + str(j)).setColor("gray")
                        else:
                            self.gui.findWidgetByID("selection_seat" + str(i) + str(j)).setColor("green")
                
                self.gui.findWidgetByID("select_seat: text").setText(
                    "Choose " + self._passengersAlt[0].getFirstName() + " " + self._passengersAlt[
                        0].getLastName() + "'s seat on " + self._selectedPaths[self._currentTripSelect].toFlights(self.fm)[0].getFullNumber())
        
    def runCheckinFindReservation(self):
        cn, ln = self.gui.findWidgetByID("checkin: reservation_number").getText(), self.gui.findWidgetByID("checkin: last_name").getText()
        try:
            self._checkinReservation = self.rm.loadReservation(cn, ln)
            # display = "Boarding pass exported to " + boardingPass.export()
            self._checkinCurrentPassenger = len(self._checkinReservation.getPassengers()) - 1
            self.gui.switchScreen("checkin_bag")
            self.runCheckinBagsNext()
        except:
            self.gui.findWidgetByID("checkin: output").setText("Invalid Reservation Number and Last Name")


    def runSelectPassengerNext(self):
        f, l = self.gui.findWidgetByID("select_passenger: first_name").getText(), self.gui.findWidgetByID(
            "select_passenger: last_name").getText()
        if len(f) == 0 or len(l) == 0:
            return
        
        if self._currentTripSelect == 0:
            self._passengers.append(Passenger(f, l))
            if len(self._passengers) == self._passengerCount:
                self.gui.switchScreen("select_seating")
                self.gui.findWidgetByID("select_passenger: first_name").setText("")
                self.gui.findWidgetByID("select_passenger: last_name").setText("")
                self.gui.findWidgetByID("select_passenger: output").setText(
                    "Fill in first and last name for passenger " + str(len(self._passengers) + 1))

                self._flightSeatingIndex, self._passengerSeatingIndex = 0, 0
                self._seatSelectionMode = 0

                # Gray out taken seats
                seatA = self.__getSeatAvailability(
                    self._selectedPaths[self._currentTripSelect].toFlights(self.fm)[self._flightSeatingIndex],
                    self._startDate, self._currentTripSelect == 0)
                for i in range(len(seatA)):
                    for j in range(len(seatA[i])):
                        if not seatA[i][j]:
                            self.gui.findWidgetByID("selection_seat" + str(i) + str(j)).setColor("gray")
                            self.gui.findWidgetByID("selection_seat" + str(i) + str(j)).toggleActivation()

                        else:
                            self.gui.findWidgetByID("selection_seat" + str(i) + str(j)).setColor("green")

                self.gui.findWidgetByID("select_seat: text").setText(
                    "Choose " + self._passengers[0].getFirstName() + " " + self._passengers[
                        0].getLastName() + "'s seat on " +
                    self._selectedPaths[self._currentTripSelect].toFlights(self.fm)[0].getFullNumber())
            else:
                self.gui.findWidgetByID("select_passenger: first_name").setText("")
                self.gui.findWidgetByID("select_passenger: last_name").setText("")
                self.gui.findWidgetByID("select_passenger: output").setText(
                    "Fill in first and last name for passenger " + str(len(self._passengers) + 1))

    def runCreateReservationSelectSeats(self, row, seat, passengerIndex):
        if self._currentTripSelect == 0:
            self._passengers[passengerIndex].addSeat(str(row + 1) + ["A", "B", "C", "D", "E", "F"][seat])
        if self._currentTripSelect == 1:
            self._passengersAlt[passengerIndex].addSeat(str(row + 1) + ["A", "B", "C", "D", "E", "F"][seat])

    def runSelectSeats(self, i):
        if i[0] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            i = i[1:]
        
        row, seat = int(i[:-1]), int(i[-1])

        if self._seatSelectionMode == 0:
            #This is creating reservation

            self.runCreateReservationSelectSeats(row, seat, self._passengerSeatingIndex)
            self._passengerSeatingIndex += 1
            if self._passengerSeatingIndex >= self._passengerCount:
                self._passengerSeatingIndex -= self._passengerCount
                self._flightSeatingIndex += 1
                if self._flightSeatingIndex == len(self._selectedPaths[self._currentTripSelect].toFlights(self.fm)):
                    #Finish selecting seats so move on to credit card
                    if self._currentTripSelect == self._tripType:
                        self.gui.switchScreen("credit_card")
                        return
                    else:
                        #Now start the inbound flight
                        self.runCreateReservationSearchFlightsAlt()
                        self._currentTripSelect = 1
                        return

            if self._currentTripSelect == 0:
                self.gui.findWidgetByID("select_seat: text").setText("Choose " + self._passengers[self._passengerSeatingIndex].getFirstName() + " " + self._passengers[self._passengerSeatingIndex].getLastName() + "'s seat on " + self._selectedPaths[self._currentTripSelect].toFlights(self.fm)[self._flightSeatingIndex].getFullNumber())
            
            if self._currentTripSelect == 1:
                self.gui.findWidgetByID("select_seat: text").setText("Choose " + self._passengers[self._passengerSeatingIndex].getFirstName() + " " + self._passengers[self._passengerSeatingIndex].getLastName() + "'s seat on " + self._selectedPaths[self._currentTripSelect].toFlights(self.fm)[self._flightSeatingIndex].getFullNumber())
        
        elif self._seatSelectionMode == 1:
            
            #Gray out taken seats
            seatA = self.__getSeatAvailability(self._selectedPaths[self._currentTripSelect].toFlights(self.fm)[self._flightSeatingIndex], self._startDate, self._currentTripSelect == 0)
            
            bad = False
            for i in range(len(seatA)):
                for j in range(len(seatA[i])):
                    if i == row and j == seat and not seatA[i][j]:
                        bad = True
                    if not seatA[i][j]:
                        self.gui.findWidgetByID("selection_seat" + str(i) + str(j)).setColor("gray")
                    else:
                        self.gui.findWidgetByID("selection_seat" + str(i) + str(j)).setColor("green")

            if bad:
                return

            self.runModifyReservationSelectSeats(row, seat, self._passengers[self._passengerSeatingIndex])
            self._passengerSeatingIndex += 1
            if self._passengerSeatingIndex == len(self._passengers):
                self.gui.switchScreen("main")
    
    #self._seatSelectionMode = 1 somewhere at the end
    def runModifyReservationFindExisting(self):
        print("Finding existing reservation.")

        cn, ln = self.gui.findWidgetByID("modify_reservation: reservation_number").getText(), self.gui.findWidgetByID(
            "modify_reservation: last_name").getText()
        reservation = self.rm.loadReservation(cn, ln)
        if reservation != 0:
            date = reservation.getFlights()[0].getDepartureDate()[0:10].lstrip("0").split("-")
            self.gui.findWidgetByID("modify_reservation_dates: start_date").setText(
                "{}/{}/{}".format(date[2], date[1], date[0]))
            self._currentReservation = reservation
            self.gui.switchScreen("modify_reservation_dates")

    def runModifyReservationChangeDate(self):
        # This is run after they enter a new date and submit it
        # self._seatSelectionMode = 1

        startdate = self.gui.findWidgetByID("modify_reservation_dates: start_date").getText()

        try:
            startdate = startdate.split("/")

            if len(startdate) != 3:
                print("Start date is invalid")
                return
            date = self._currentReservation.getFlights()[0].getDepartureDate()[0:10].lstrip("0").split("-").reverse()

            if date != startdate:
                self._seatSelectionMode = 1

                totalFlightTime = 0
                setStartDate(int(startdate[2]), int(startdate[0]), int(startdate[1]))

                for i in range(len(self._currentReservation.getFlights())):
                    flightNumber = self._currentReservation.getFlights()[i].getNumber()
                    flightDestinationCode = self._currentReservation.getFlights()[i].getDestination()[-4:-1]
                    flight = self.fs.searchForFlight(flightDestinationCode,flightNumber)

                    nextFlightTime = flight.timeUntilNextFlight(offsetStartTime(timedelta(hours=totalFlightTime)))
                    flightTime = flight.getTravelTime()

                    totalFlightTime += nextFlightTime + flightTime

                newTime = self._currentReservation.getFlights()[0].getDepartureDate()
                newTime.replace(year=int(startdate[2]), month = int(startdate[0]), day = int(startdate[1]))

                tempRes = self.rm.createReservation()

                for flight in self._currentReservation.getFlights():
                    tempRes.addFlight(flight, newTime)

                for passenger in self._currentReservation.getPassengers():
                    tempRes.addPassenger(passenger)

                self.rm.serializeAll()

                # TODO user selects a new seat
                self.gui.switchScreen("select_seating")
            else:
                # TODO no date change user selects new seat if they want
                self.gui.switchScreen("select_seating")



        except ValueError:
            print("Input is invalid")

    def runCreditCardCreateReservation(self):
        cardIsValid = self.rm.validateCreditCard(self.gui.findWidgetByID("credit_card: creditcard").getText())
        if not cardIsValid:
            self.gui.findWidgetByID("credit_card: output").setText("Invalid credit card - try again.")
            return

        self._currentReservation = self.rm.createReservation()
        self._currentReservation.setFlights(self.singleFlights)
        for passenger in self._passengers:
            self._currentReservation.addPassenger(passenger)
        self._currentReservation.matchSeats()

        if self._tripType == 1:
            self._currentReservationAlt = self.rm.createReservation()
            self._currentReservationAlt.setFlights(self.singleFlightsAlt)
            for passenger in self._passengersAlt:
                self._currentReservationAlt.addPassenger(passenger)
            self._currentReservationAlt.matchSeats()

        self.rm.serializeAll()
        self.singleFlights, self.singleFlightsAlt = [], []

        print("Created reservation")

        self.gui.switchScreen("create_reservation_success")
        self.runCreateReservationSuccess()
        self._start, self._end = 0, 0
        self.gui.findWidgetByID("create_reservation: start").setText("")
        self.gui.findWidgetByID("create_reservation: destination").setText("")
        self.gui.findWidgetByID("create_reservation: travelers").setText("")
        self.gui.findWidgetByID("create_reservation: return_date").setText("")
        self.gui.findWidgetByID("create_reservation: start_date").setText("")
        self.gui.findWidgetByID("create_reservation: output").setText("")
        self.gui.findWidgetByID("select_passenger: first_name").setText("")
        self.gui.findWidgetByID("select_passenger: last_name").setText("")

    def runCreateReservationSuccess(self):
        reservationInfo = "Last Name: " + self._currentReservation.getLastName() + "\n"

        if self._tripType == 0:
            self.gui.findWidgetByID("Success_Description").setText("A one-way reservation has been created.")
            reservationInfo += "Confirmation Number: " + self._currentReservation.getConfirmationNumber()
        else:
            self.gui.findWidgetByID("Success_Description").setText("A round-trip reservation has been created.")
            reservationInfo += "Outbound Confirmation Number: " + self._currentReservation.getConfirmationNumber() + "\n"
            reservationInfo += "Inbound Confirmation Number: " + self._currentReservationAlt.getConfirmationNumber()

        self.gui.findWidgetByID("create_reservation_success: display_info").setText(reservationInfo)

    def runModifyReservationSelectSeats(self, row, seat, passenger):
        # This is run after a seat is selected for modify reservation.
        self._currentReservation.modifySeat(row, seat, passenger.getFirstName(), passenger.getLastName(),
                                            self._flightSeatingIndex)

    def runCheckinBagsNext(self):
        if self._checkinReservation == None:
            self.gui.switchScreen("main")
            return
        self.gui.findWidgetByID("checkin_bags: output").setText("Enter Number of Bags to Check-In for " +
                                                                self._checkinReservation.getPassengers()[
                                                                    self._checkinCurrentPassenger].getFirstName() + " " +
                                                                self._checkinReservation.getPassengers()[
                                                                    self._checkinCurrentPassenger].getLastName())
        self._checkinCurrentPassenger -= 1
        if self._checkinCurrentPassenger >= -1:
            try:
                if self.gui.findWidgetByID("checkin_bags: bags").getText() == "":
                    return
                else:
                    x = int(self.gui.findWidgetByID("checkin_bags: bags").getText())
                    if x < 1:
                        self.gui.findWidgetByID("checkin_bags: output").setText("Invalid Number of Bags")

            except ValueError:
                self.gui.findWidgetByID("checkin_bags: output").setText("Invalid Number of Bags")
        else:
            BoardingPass(self._checkinReservation)
            self.gui.findWidgetByID("checkin_bags: output").setText(
                "Boarding Passes Generated for " + self._checkinReservation.getConfirmationNumber())
            self._checkinReservation, self._checkinCurrentPassenger = None, 0
            self.gui.findWidgetByID("checkin: output").setText("")
            self.gui.findWidgetByID("checkin: reservation_number").setText("")
            self.gui.findWidgetByID("checkin: last_name").setText("")
            self.gui.findWidgetByID("checkin_bags: bags").setText("")

    def __getSeatAvailability(self, flightId, depDate, isOutbound):
        singleFlight = self.rm.createSingleFlight(flightId, depDate)

        if isOutbound:
            self.singleFlights.append(singleFlight)
        else:
            self.singleFlightsAlt.append(singleFlight)

        return singleFlight.getAvailableSeats()