# Name: Graph.py
# Description: Implements a graph.

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/15/20		Original
# 1.1   Joseph Liu              05/20/20		Add edges

import heapq
import math

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
            self.ntoa[i] = a[i].getId()
            self.aton[a[i].getId()] = i
        
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
    
    def reset(self):
        for node in self.nodes:
            node.reset(self.MAX)
            

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
        self.dist = math.ceil(d * 1000) / 1000

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
        self.r = False
    
    def removed(self):
        return self.r