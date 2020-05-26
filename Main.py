# Name: Main.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0       Christopher Luey        05/17/20		Original
# 1.1       Christopher Luey        05/17/20		Compatibility with widget id system


from UI.GUI import GUI
from flights.FlightSearcher import *


def main():
    # fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    # fs = FlightSearcher(fm)


    gui = GUI()
    clicked = 0
    screens = gui.getScreenIDs()

    while clicked != 'quit':
        screen = gui.getScreen()
        clicked = gui.setOnButtonClickListener()
        if clicked == 'quit':
            break
        print("ID:", clicked, "- Action Performed")
        if clicked in screens or clicked == 'back':
            gui.switchScreen(clicked)
        else:
            print("ID:", clicked, "- Not Switch Screen")




def test():
    fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    fs = FlightSearcher(fm)
    inp = ""
    while inp != "quit":
        inp = input(">>> ").lower()
        t = inp.split()
        print(t)
        try:
            if t[0] == "search":
                if t[1] == "airport":
                    for airport in fs.searchForAirports(t[2]): #Returns 10 airports with char
                        print(airport.toString())
                elif t[1] == "flight":
                    if len(t) == 4:
                        t.append(5)
                    for airport in fs.searchForFlights(fs.searchForAirports(t[2])[0], fs.searchForAirports(t[3])[0],int(t[4]))[0].toFlights(fm):
                        print(airport.toString())
        except IndexError:
            print("Invalid command")


if __name__ == '__main__':
    main()
    #test()


