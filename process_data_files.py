import unidecode
from flights.Airport import *
from unprocessed_data._Flight import *


def readFile(fileName, hasSymbols):
    if hasSymbols:
        f = open(fileName, "r", encoding="utf-8")
    else:
        f = open(fileName, "r")
    
    s = f.readlines()
    f.close()

    out = []
    for line in s:
        l = unidecode.unidecode(line).split("\t")
        for i in range(len(l)):
            l[i] = l[i].strip("\t, \"\n")
        out.append(l)
    
    return out

def getTimezones(fileContent):
    tz = {}
    for row in fileContent:
        tz[row[0]] = row[1]
    
    return tz

def createAirports(fileContent, timezones):
    airports = []
    codes = {}
    index = 0
    sizes = ["small_airport", "medium_airport", "large_airport", "closed", "heliport", "seaplane_base", "balloonport"]
    used = []

    for l in fileContent:
        if len(l[13]) == 3:
            #__init__(code, city, name, timezone, size)
            airports.append(Airport(l[13], l[10], l[3], "none", sizes.index(l[2])))
            used.append(l[13])
            codes[airports[-1].getCode()] = index
            index += 1

    for l in fileContent:
        if len(l[14]) == 3 and l[14] not in used:
            #__init__(code, city, name, timezone, size)
            airports.append(Airport(l[14], l[10], l[3], "none", sizes.index(l[2])))
            used.append(l[14])
            codes[airports[-1].getCode()] = index
            index += 1
    
    n = []
    index = 0
    for airport in airports:
        if airport.code in timezones:
            airport.timezone = timezones[airport.code]
            n.append(airport)
            codes[airport.code] = index
            index += 1
    
    airports = n
    return airports, codes

def createFlights(fileContent, airports, codes):
    index = 0
    processed = []
    flights = []
    serviced = {}

    for l in fileContent:
        if l[4] + l[5] in processed:
            continue
        processed.append(l[4] + l[5])
        
        flights.append(Flight(index, l[4], int(l[5]), airports[codes[l[0]]], airports[codes[l[1]]], l[2], l[3], l[6]))
        flights[-1].getOrigin().addFlight(flights[-1])
        flights[-1].getDestination().addFlight(flights[-1])

        serviced[l[1]] = True
        serviced[l[0]] = True
        index += 1
    
    return flights, serviced

def clean(airports, flights, serviced, timezones, codes):
    a = []
    for airport in airports:
        #To be a valid airport, it needs to be serviced and have a valid time zone.
        if airport.code in serviced and airport.code in timezones and airport.timezone != "none":
            a.append(airport)
        else:
            #print("Airport", airport.code, "not serviced.")
            continue
    
    return a

def writeToFiles(a, f):
    fa, ff = open("data/airports.tsv", "w"), open("data/flights.tsv", "w")

    fa2 = "Code\tTimezone\tName\tCity\tSize\n"
    for a2 in a:
        fa2 += a2.code + "\t" + a2.timezone + "\t" + a2.name + "\t" + a2.city + "\t" + str(a2.size) + "\n"
    fa.write(fa2[:-1])
    fa.close()

    ff2 = "Source\tDest\tLeave\tArrive\tCarrier\tFlight\tDays\n"
    for f2 in f:
        #Source	Destination	Leave	Arrive	Carrier	Flight	Days
        ff2 += f2.getOrigin().getCode() + "\t" + f2.getDestination().getCode() + "\t" + f2.departureTime + "\t" + f2.arrivalTime + "\t" + f2.airline + "\t" + str(f2.number) + "\t" + f2.days + "\n"
    ff.write(ff2[:-1])
    ff.close()

def main():
    print("Reading files...")

    airports = readFile("unprocessed_data/airports2.unprocessed", True)[1:]
    print("Read file 1/3")

    flights = readFile("unprocessed_data/flights2.unprocessed", True)[1:]
    print("Read file 2/3")

    timezones = readFile("unprocessed_data/tz.unprocessed", True)
    print("Read file 3/3")
    
    print("Processing timezones...")
    tz = getTimezones(timezones)

    print("Creating airports...")
    a, c = createAirports(airports, tz)

    print("Creating flights...")
    f, s = createFlights(flights, a, c)

    print("Cleaning data...")
    a = clean(a, f, s, tz, c)

    print("Writing data to files...")
    writeToFiles(a, f)

    print("Done processing data files.")

main()