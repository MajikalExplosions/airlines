# Name: DijkstraSP.py
# Description: Finds the shortest path between two airports using Dijkstra's algorithm

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/15/20		Original
# 2.0   Joseph Liu              05/20/20		Reimplemented without getting node from airport
# 3.0   Joseph Liu              05/23/20		Update time spent calculations and reimplement with path object

import heapq
from flights.paths.Graph import Graph
from flights.Time import *
from datetime import timedelta
from flights.paths.Path import Path
from time import time

class DijkstraSP:
    def __init__(self, graph, origin, target, rootVal = 0):
        nodes = graph.getNodes()
        pq = [(0, origin)]
        origin.root(rootVal)
        origin.v = False
        heapq.heapify(pq)
        
        while len(pq) > 0:
            cur = heapq.heappop(pq)
            
            cur[1].visit()

            if cur[1] == target:
                break
            
            for edge in cur[1].getEdges():
                if not graph.exists(edge.v) or edge.removed():
                    continue
                dest = nodes[edge.v]
                #1 is added because layovers take T I M E
                timeSpent = edge.f.getTravelTime() + edge.f.timeUntilNextFlight(offsetStartTime(timedelta(hours=cur[1].getDist() + 1)))
                
                #If new path shorter, update.
                if cur[1].getDist() + timeSpent < dest.getDist():
                    dest.setDist(cur[1].getDist() + timeSpent)
                    dest.setEdgeIn(edge)
                    heapq.heappush(pq, (cur[1].getDist() + timeSpent, dest))
        
        self.dest = target
        self.graph = graph
    
    def getPath(self):
        if not self.dest.visited():
            return (False, 0)
        p = Path()
        p.fromDSP(self, self.dest)
        return True, p
