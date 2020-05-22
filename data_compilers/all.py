from Airport import Airport
from Flight import Flight

class All:
    def __init__(self):
        self.flights = []
        self.airports = []
        codes = {}
        processed = []

        af = open("airports_all.tsv", "r")
        contents = af.readlines()[1:]
        af.close()
        index = 0
        for line in contents:
            l = line.split("\t")
            for i in range(len(l)):
                l[i] = l[i].strip()
            self.airports.append(Airport(l[0], l[3], l[2], l[1]))
            codes[self.airports[-1].getCode()] = index
            index += 1

        ff = open("flights_all.tsv", "r")
        contents = ff.readlines()[1:]
        ff.close()
        index = 0
        for line in contents:
            l = line.split("\t")
            for i in range(len(l)):
                l[i] = l[i].strip()
            if l[4] + l[5] in processed:
                continue
            processed.append(l[4] + l[5])
            #print(processed)
            self.flights.append(Flight(index, l[4], int(l[5]), self.airports[codes[l[0]]], self.airports[codes[l[1]]], l[2], l[3], l[6]))
            self.flights[-1].getOrigin().addFlight(self.flights[-1])
            self.flights[-1].getDestination().addFlight(self.flights[-1])
            index += 1

        n = []
        for a in self.airports:
            if a.hasFlight():
                n.append(a)
        self.airports = n

        print("Done processing. Flights:", len(self.flights), "| Airports:", len(self.airports))

        flightString = ""
        for flight in self.flights:
            flightString += str(flight.getOrigin().getCode()) + "\t" + str(flight.getDestination().getCode()) + "\t" + flight.getDepTime() + "\t" + flight.getArrTime() + "\t" + flight.airline + "\t" + str(flight.number) + "\t" + flight._temp + "\n"
        ff = open("flights.tsv", "w")
        ff.write(flightString)
        ff.close()

        airportString = ""
        for airport in self.airports:
            airportString += str(airport.code) + "\t" + str(airport.timezone) + "\t" + airport.name + "\t" + airport.city + "\n"
        af = open("airports.tsv", "w")
        af.write(airportString)
        af.close()

All()