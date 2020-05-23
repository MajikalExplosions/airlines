# Name: DijkstraSP.py
# Description: Finds the shortest path between two airports using Dijkstra's algorithm

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/15/20		Original

import heapq
from Reservation.Path.Graph import Graph
import FlightManager

class DijkstraSP:
    def __init__(self, graph, origin):
        nodes = graph.getNodes()

        pq = [(0, origin.getNode())]
        origin.getNode().root()
        heapq.heapify(pq)
        
        while len(pq) > 0:
            cur = heapq.heappop(pq)
            if cur[1].visited():
                continue

            cur[1].visit()
            for f in cur[1].getEdges():
                #print(f.toString())
                dest = f.getDestination().getNode()
                #At some point we may want to add the layover times to the following calculation.
                timeSpent = f.getTravelTime()

                #If new path shorter, update.
                tt = cur[1].getDist()
                if tt + timeSpent < dest.getDist():
                    dest.setDist(tt + timeSpent)
                    dest.setFlightIn(f)
                    heapq.heappush(pq, (tt + timeSpent, f.getDestination().getNode()))
        
        self.graph = graph
    
    def getPath(self, dest):
        cur = dest.getNode()
        path = []
        while not cur.isRoot():
            if cur.getFlightIn() in path:
                break
            path.insert(0, cur.getFlightIn())
            for f in cur.getAirport().getFlights():
                #print(f.toString(), f.getTravelTime())
                pass
            cur = cur.getFlightIn().getOrigin().getNode()
        
        return path

def test():
    fm = FlightManager.FlightManager("data_compilers/airports.tsv", "data_compilers/flights.tsv")
    graph = Graph(fm)
    sp = DijkstraSP(graph, fm.airports[69])
    print("Path from", fm.airports[69].getName(), "to", fm.airports[419].getName(), "takes", fm.airports[419].getNode().dist, "hours")

    for f in sp.getPath(fm.airports[419]):
        print(f.toString())
    #print(sp.getPath(fm.airports[12]))

if __name__ == "__main__":
    test()