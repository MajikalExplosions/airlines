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
        self.ntoa = {}
        self.aton = {}

    def fromFlights(self, fm):
        a = fm.getAirports()
        for i in range(len(a)):
            self.nodes.append(Node(i, self.MAX))
            self.ntoa[i] = a.getId()
            self.aton[a.getId()] = i
        
        for airport in a:
            for flight in airport.getFlights():
                self.aton[airport.getId()].addEdge(Edge(flight, airport.getId(), self.aton[flight.getDestination().getId()]))

    def removeEdges(self, remove):
        for e in remove:
            self.nodes[e.u].getEdges().remove(e)
    
    def addEdges(self, add):
        for e in add:
            self.nodes[e.u].addEdge(e)
    
    def removeNodes(self, remove):
        for n in remove:
            self.nodes[n.nid] = 0
    
    def addNodes(self, add):
        for n in add:
            self.nodes[n.nid] = n

    def getNodes(self):
        return self.nodes
    
    def exists(self, id):
        return self.nodes[id] == 0
            

class Node:
    def __init__(self, i, m):
        self.nid = i
        #Dijkstra stuff
        self.reset(m)
        self.v = False
        self.edges = []
    
    def addEdge(self, e):
        self.edges.append(e)

    def getEdges(self):
        return self.edges
    
    def getDist(self):
        return self.dist
    
    def setDist(self, d):
        self.dist = d

    def visited(self):
        return self.v
    
    def visit(self):
        self.v = True
    
    def reset(self, mx):
        self.dist = mx
        self.edgeIn = 0
        self.v = False
    
    def setEdgeIn(self, p):
        self.edgeIn = p

    def getEdgeIn(self):
        return self.edgeIn
    
    def isRoot(self):
        return self.edgeIn == -1

    def root(self):
        self.dist = 0
        self.edgeIn = -1

    def __lt__(self, o):
        return 0
    
class Edge:
    def __init__(self, flight, start, end):
        self.f = flight
        self.u = start
        self.v = end