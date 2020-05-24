# Name: Path.py
# Description: Represents a path object

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/23/20		Original

from Flight.paths.Graph import *

class Path:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.dist = -1
        self.graph = 0
    
    def fromDSP(self, dsp, dest):
        try:
            self.nodes = [dest]
            self.edges = []
            while not self.nodes[0].isRoot():
                self.edges.insert(0, self.nodes[0].getEdgeIn())
                self.nodes.insert(0, dsp.graph.getNodes()[self.nodes[0].getEdgeIn().u])
            
            self.dist = dest.dist
            self.graph = dsp.graph
        except:
            self.nodes = []
            self.edges = []
            self.dist = -1
            print("Bad.")
            return
    
    def fromTwo(self, p1, p2):
        #Combines to paths.
        #Assumes that the p1 ends on the same node that p2 starts at.
        if p1.getNodes()[-1] != p2.getNodes()[0]:
            print("Can't combine two paths.")
            print(p1.getNodes(), p2.getNodes())
            return
        self.nodes = p1.getNodes()[:-1] + p2.getNodes()
        self.edges = p1.getEdges() + p2.getEdges()
        self.dist = p1.dist + p2.dist
        self.graph = p1.graph

    def sliceToPath(self, i1, i2):
        #Gets a slice of the original path between the i1th node and i2th node, inclusive
        np = Path()
        nn = self.nodes[i1:i2 + 1]
        ne = self.edges[i1:i2]
        np.nodes = nn
        np.edges = ne
        np.dist = nn[-1].dist - nn[0].dist
        np.graph = self.graph
        return np

    def getNodes(self):
        return self.nodes
    
    def getEdges(self):
        return self.edges

    def getDist(self):
        return self.dist

    def toString(self, fm):
        s = ""
        for i in range(len(self.edges)):
            s += "Arrival at " + fm.getAirport(self.graph.ntoa[self.nodes[i].nid]).toString() + " at " + str(self.nodes[i].dist) + "\n"
            s += "Take " + self.edges[i].f.toString() + "\n"
        
        s += "Final arrival at " + fm.getAirport(self.graph.ntoa[self.nodes[-1].nid]).toString() + " at " + str(self.dist)
        return s

    def equals(self, other):
        p1 = self.edges
        p2 = other.edges
        if len(p1) != len(p2):
            return False
        
        for i in range(len(p1)):
            if p1[i].f != p2[i].f:
                return False
        
        return True