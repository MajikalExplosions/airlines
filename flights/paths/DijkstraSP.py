# Name: DijkstraSP.py
# Description: Finds the shortest path between two airports using Dijkstra's algorithm

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/15/20		Original
# 1.0   Joseph Liu              05/20/20		Reimplemented without getting node from airport

import heapq
from flights.paths.Graph import Graph
from flights.Time import *
from datetime import timedelta


class DijkstraSP:
    def __init__(self, graph, origin):
        nodes = graph.getNodes()

        pq = [(0, origin)]
        origin.root()
        heapq.heapify(pq)
        
        while len(pq) > 0:
            cur = heapq.heappop(pq)
            if cur[1].visited():
                continue

            cur[1].visit()
            for edge in cur[1].getEdges():
                if not graph.exists(edge.v):
                    continue
                dest = nodes[edge.v]
                #At some point we want to add the layover times to the following calculation.
                timeSpent = edge.f.getTravelTime() + edge.f.timeUntilNextFlight(offsetStartTime(timedelta(hours=cur[1].getDist())))

                #If new path shorter, update.
                if cur[1].getDist() + timeSpent < dest.getDist():
                    dest.setDist(cur[1].getDist() + timeSpent)
                    dest.setEdgeIn(edge)
                    heapq.heappush(pq, (cur[1].getDist() + timeSpent, dest))
        
        self.graph = graph
    
    def pathIsEqual(self, other, dest, i):
        p1 = self.getPathEdge(dest)
        p2 = other.getPathEdge(dest)
        for x in range(i):
            if p1[x].f != p2[x].f:
                return False
        
        return True
    
    def getPathEdge(self, dest):
        path = [dest.getEdgeIn()]
        while not self.graph.getNodes()[path[0].u].isRoot():
            path.insert(0, self.graph.getNodes()[path[0].u].getEdgeIn())
        
        return path
    
    def getPathNode(self, dest):
        path = [dest]
        while not path[0].isRoot():
            path.insert(0, self.graph.getNodes()[path[0].getEdgeIn().u])
        
        return path
