import unidecode

class Airport:
    def __init__(self, code, name, city):
        self.code = code.strip("\" ,\t\n")
        self.name = name.strip("\" ,\t\n")
        self.city = city.strip("\" ,\t\n")
        self.tz = ""
    
    def addTimezone(self, tz):
        self.tz = tz.strip("\" ,\t\n")
    
    def good(self):
        return len(self.code) > 0 and len(self.tz) > 0
    def toString(self):
        return self.code + "\t" + self.tz + "\t" + self.name + "\t" + self.city
    
    def key(self):
        return self.code

f1, f2 = open("airports.unprocessed", "r", encoding="utf-8"), open("tz.unprocessed", "r")
names = f1.readlines()[1:]
tzs = f2.readlines()
f1.close()
f2.close()

airports = []
used = []
for row in names:
    row = row.split(",")
    if len(row[13].strip("\" ,\t\n")) == 3:
        airports.append(Airport(row[13].strip("\" ,\t\n"), row[3].strip("\" ,\t\n"), row[10].strip("\" ,\t\n")))
        used.append(row[13].strip("\" ,\t\n"))

for row in names:
    row = row.split(",")
    code = row[14].strip("\" ,\t\n")
    if len(code) == 3 and (code not in used):
        airports.append(Airport(code, row[3].strip("\" ,\t\n"), row[10].strip("\" ,\t\n")))
        used.append(code)

airports.sort(key=Airport.key)

for i in range(len(tzs)):
    tzs[i] = tzs[i].strip("\" ,\t\n").split()

i1, i2 = 0, 0
while i1 < len(airports) and i2 < len(tzs):
    c1, c2 = airports[i1].code, tzs[i2][0].strip("\" ,\t\n")
    if c1 == c2:
        airports[i1].addTimezone(tzs[i2][1].strip("\" ,\t\n"))
        i1 += 1
        i2 += 1
    elif c1 < c2:
        #print(airports[i1].code)
        i1 += 1
    elif c1 > c2:
        print(airports[i1].code)
        i2 += 1

out = open("airports.tsv", "w", encoding="utf-8")
out.write("IATA\tTimezone\tAirport Name\tCity\n")
for airport in airports:
    if airport.good():
        out.write(unidecode.unidecode(airport.toString()) + "\n")
        #out.write(airport.toString() + "\n")

out.close()