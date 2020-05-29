# Name: Path.py
# Description: Represents a path object

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/23/20		Original

from flights.paths.Graph import *
from datetime import timedelta
from flights.Time import *


class Path:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.distToNode = []
        self.graph = 0
    
    def fromDSP(self, dsp, dest):
        self.nodes = [dest]
        self.edges = []
        while not self.nodes[0].isRoot():
            self.edges.insert(0, self.nodes[0].getEdgeIn())
            self.nodes.insert(0, dsp.graph.getNodes()[self.nodes[0].getEdgeIn().u])
        
        self.distToNode = []
        for node in self.nodes:
            self.distToNode.append(node.getDist())
        
        self.graph = dsp.graph
    
    def fromTwo(self, p1, p2):
        #Combines to paths.
        #Assumes that the p1 ends on the same node that p2 starts at.
        if p1.getNodes()[-1] != p2.getNodes()[0]:
            print("Can't combine two paths.")
            return
        self.nodes = p1.getNodes()[:-1] + p2.getNodes()
        self.distToNode = p1.getDists()[:-1]
        self.edges = p1.getEdges() + p2.getEdges()
        
        offset = p1.getNodes()[-1].getDist() - p2.getNodes()[0].getDist()
        for d in p2.getDists():
            self.distToNode.append(d + offset)

        self.graph = p1.graph

    def sliceToPath(self, i1, i2):
        #Gets a slice of the original path between the i1th node and i2th node, inclusive
        np = Path()
        nn = self.nodes[i1:i2 + 1]
        ne = self.edges[i1:i2]
        np.nodes = nn
        np.edges = ne
        np.distToNode = self.distToNode[i1:i2 + 1]
        np.graph = self.graph
        return np

    def getNodes(self):
        return self.nodes
    
    def getEdges(self):
        return self.edges

    def getDists(self):
        return self.distToNode

    def toShortString(self, fm):
        if len(self.toAirports(fm)) == 0:
            return "Empty path."
        s = str(round(self.timeToNodeArrival(-1, fm), 2)) + " hrs: "
        for a in self.toAirports(fm):
            s += a.getCode() + " - "
        s = s[:-3] + "\n"
        for f in self.toFlights(fm):
            s += f.getAirline() + str(f.getNumber()) + " - "
        return s[:-3]


    def toString(self, fm):
        s = ""
        for i in range(len(self.edges)):
            s += "Arrival at " + fm.getAirport(self.graph.ntoa[self.nodes[i].nid]).toString() + " at " + str(self.distToNode[i]) + "\n"
            s += "Take " + self.edges[i].f.toString() + "\n"
        
        s += "Final arrival at " + fm.getAirport(self.graph.ntoa[self.nodes[-1].nid]).toString() + " at " + str(self.distToNode[-1])
        return s
    
    def recalculateDist(self, initial):
        self.distToNode = [initial]
        for i in range(len(self.edges)):
            nextFlightTime = self.edges[i].f.timeUntilNextFlight(offsetStartTime(timedelta(hours=self.distToNode[-1])))
            flightTime = self.edges[i].f.getTravelTime()
            self.distToNode.append(self.distToNode[-1] + nextFlightTime + flightTime)
    
    def toAirports(self, fm):
        a = []
        for i in range(len(self.nodes)):
            a.append(fm.getAirport(self.graph.ntoa[self.nodes[i].nid]))
        return a

    def toFlights(self, fm):
        f = []
        for i in range(len(self.edges)):
            f.append(self.edges[i].f)
        return f

    def timeToNodeDeparture(self, index):
        return self.distToNode[index]
    
    def timeToNodeArrival(self, index, fm):
        if index == 0:
            return 0
        
        if index == -1 or index >= len(self.distToNode) - 1:
            return self.distToNode[-1]
        arriveLast = self.distToNode[index - 1]
        flightToCurrent = self.toFlights(fm)[index - 1].getTravelTime()
        return arriveLast + flightToCurrent

    def equals(self, other):
        p1 = self.edges
        p2 = other.edges
        if len(p1) != len(p2):
            return False
        
        for i in range(len(p1)):
            if p1[i].f != p2[i].f:
                return False
        
        return True