#Put test programs here because this is where you need to run it from for it to work.

from flights.FlightManager import *
from flights.paths.DijkstraSP import *
from flights.paths.Graph import *

def test():
    fm = FlightManager("Data/airports.tsv", "Data/flights.tsv")
    graph = Graph(fm)
    sp = DijkstraSP(graph, fm.airports[69])
    print("Path from", fm.airports[69].getName(), "to", fm.airports[419].getName(), "takes", fm.airports[419].getNode().dist, "hours")

    for f in sp.getPath(fm.airports[419]):
        print(f.toString())
    #print(sp.getPath(fm.airports[12]))

if __name__ == "__main__":
    test()