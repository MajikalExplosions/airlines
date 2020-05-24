#Put test programs here because this is where you need to run it from for it to work.

from flights.FlightManager import *
from flights.paths.DijkstraSP import *
from flights.paths.Graph import *
from datetime import timedelta

def test(a, b):
    fm = FlightManager("data/airports.tsv", "data/flights.tsv")
    graph = Graph()
    graph.fromFlights(fm)

    sp = DijkstraSP(graph, graph.getNodeFromAirport(fm.airports[a]))
    print("\nPath from", fm.airports[a].getName(), "to", fm.airports[b].getName(), "takes", graph.getNodeFromAirport(fm.airports[b]).dist, "hours\n")

    for node in sp.getPathNode(graph.getNodeFromAirport(fm.airports[b])):
        print("Arrival at", fm.getAirport(graph.ntoa[node.nid]).getSearchString(), "at", offsetStartTime(timedelta(hours=round(node.dist, 3))))
    
    print()
    for edge in sp.getPathEdge(graph.getNodeFromAirport(fm.airports[b])):
        print("Take", edge.f.toString())
    #print(sp.getPath(fm.airports[12]))

if __name__ == "__main__":
    test(1, 3)