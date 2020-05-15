# Name: DijkstraSP.py
# Description: Finds the shortest path between two airports using Dijkstra's algorithm

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/15/20		Original

import heapq
import ShortestPathTree

class DijkstraSP:
    def __init__(self, graph, origin):
        nodes = graph.getNodes()

        pq = [(0, origin.getNode())]
        heapq.heapify(pq)
        
        while len(pq) > 0:
            cur = heapq.heappop(pq)
            if cur[1].visited():
                continue

            cur[1].visit()
            for f in cur[1].getEdges():
                dest = f.getDestination().getNode()
                #At some point we may want to add the layover times to the following calculation.
                timeSpent = f.getTravelTime()

                #If new path shorter, update.
                if f.getDist() + timeSpent < dest.getDist():
                    dest.setDist(f.getDist() + timeSpent)
                    dest.setFlightIn(f)
                    heapq.heappush(pq, (f.getDist() + timeSpent, f.getDestination().getNode()))
        
        self.grapth = graph
    
    def getPath(self, dest):
        cur = dest
        path = []
        while not cur.isRoot():
            path.insert(0, cur.getFlightIn())
            cur = cur.getFlightIn().getOrigin().getNode()
        
        return path