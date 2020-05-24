# Name: Graph.py
# Description: Implements a graph.

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/15/20		Original

import heapq

class Graph:
    def __init__(self, fm):
        self.nodes = []
        self.MAX = 1000000000
        airports = fm.getAirports()
        for i in range(len(airports)):
            self.nodes.append(Node(i, airports[i], self.MAX))
    
    def getNodes(self):
        return self.nodes
            

class Node:
    def __init__(self, i, a, m):
        self.nid = i
        self.airport = a
        a.setNode(self)
        #Dijkstra stuff
        self.reset(m)
        self.v = False
    
    def getEdges(self):
        return self.airport.getFlights()

    def getAirport(self):
        return self.airport
    
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
        self.flightIn = 0
        self.v = False
    
    def setFlightIn(self, p):
        self.flightIn = p

    def getFlightIn(self):
        return self.flightIn
    
    def isRoot(self):
        return self.flightIn == -1

    def root(self):
        self.dist = 0
        self.flightIn = -1

    def __lt__(self, o):
        return 0