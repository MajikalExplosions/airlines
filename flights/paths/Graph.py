# Name: Graph.py
# Description: Implements a graph.

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/15/20		Original
# 1.1   Joseph Liu              05/20/20		Add edges

import heapq

class Graph:
    def __init__(self):
        self.nodes = []
        self.MAX = 1000000000

        #Maps between node id and airport ids
        self.ntoa = {}
        self.aton = {}

    def fromFlights(self, fm):
        a = fm.getAirports()
        
        #First create all nodes and map ids to each other
        for i in range(len(a)):
            self.nodes.append(Node(i, self.MAX))
            self.ntoa[i] = a[i].getId()
            self.aton[a[i].getId()] = i
        
        #Add edges representing each flight
        for airport in a:
            for flight in airport.getFlights():
                self.nodes[self.aton[airport.getId()]].addEdge(Edge(flight, self.aton[airport.getId()], self.aton[flight.getDestination().getId()]))

    def removeEdges(self, remove):
        for e in remove:
            e.r = True
    
    def addEdges(self, add):
        for e in add:
            e.r = False

    def getNodes(self):
        return self.nodes
    
    def getNodeFromAirport(self, a):
        return self.nodes[self.aton[a.getId()]]

    def exists(self, i):
        return self.nodes[i] != 0
    
    def resetAll(self):
        for node in self.nodes:
            node.reset(self.MAX)
    
    def reset(self, path):
        #Resets all nodes except for those in path
        for node in self.nodes:
            if node not in path.getNodes():
                node.reset(self.MAX)
            else:
                node.q = self.MAX
            

class Node:
    def __init__(self, i, m):
        self.nid = i
        #Dijkstra stuff
        self.reset(m)
        self.v = False
        self.q = m
        self.edges = []
    
    def addEdge(self, e):
        self.edges.append(e)

    def getEdges(self):
        return self.edges
    
    def getDist(self):
        return self._dist
    
    def setDist(self, d):
        self._dist = d

    def visited(self):
        return self.v
    
    def getQ(self):
        #Whether it's in the queue or not
        return self.q

    def setQ(self, q):
        self.q = q
    
    def inQ(self):
        return self.q < 1000000
    
    def rmQ(self):
        self.q = 1000000
    
    def visit(self):
        self.v = True
    
    def reset(self, mx):
        self._dist = mx
        self.edgeIn = 0
        self.v = False
        self.q = mx
    
    def setEdgeIn(self, p):
        #Sets the edge/flight that was taken to arrive at this node
        self.edgeIn = p

    def getEdgeIn(self):
        return self.edgeIn
    
    def isRoot(self):
        return self.edgeIn == -1

    def root(self, d):
        #Sets this node as the root node
        self._dist = d
        self.edgeIn = -1

    def __lt__(self, o):
        return 0
    
class Edge:
    def __init__(self, flight, start, end):
        self.f = flight
        self.u = start
        self.v = end
        self.r = False
    
    def removed(self):
        #r represents whether this edge/flight should be traveled or not
        return self.r