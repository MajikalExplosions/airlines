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
        pq = [(rootVal, origin)]
        origin.root(rootVal)
        origin.v = False
        origin.setQ(rootVal)
        heapq.heapify(pq)

        #Whether to manage the heap or not; it's slow if you do but takes less memory.
        self.manage = False
        
        while len(pq) > 0:
            #Get the closest airport/node in the queue
            cur = heapq.heappop(pq)
            
            #Visit said node and remove it from the queue.
            cur[1].visit()
            cur[1].rmQ()

            #If we've found the target, then the search is over
            if cur[1] == target:
                break
            
            for edge in cur[1].getEdges():
                #Remove
                if not graph.exists(edge.v) or edge.removed():
                    continue
                dest = nodes[edge.v]
                #1 is added because layovers take T I M E
                timeSpent = edge.f.getTravelTime() + edge.f.timeUntilNextFlight(offsetStartTime(timedelta(hours=cur[1].getDist() + 1)))
                
                #If new path shorter, update.
                if cur[1].getDist() + timeSpent < dest.getDist():
                    dest.setDist(cur[1].getDist() + timeSpent)
                    dest.setEdgeIn(edge)

                    #If it's in queue and this new one is better, update.
                    if dest.inQ() and self.manage:
                        #This only runs if I'm managing the queue, which I'm not.
                        if cur[1].getDist() + timeSpent < dest.getQ():

                            #Find its location in queue
                            ind = -1
                            for i in range(len(pq)):
                                if pq[i][1] == dest:
                                    ind = i
                            if ind == -1:
                                print("Uh oh.")
                                print(dest.getQ())

                            #Remove from queue and add new key
                            pq = pq[:ind] + pq[ind + 1:]
                            heapq.heapify(pq)
                            heapq.heappush(pq, (cur[1].getDist() + timeSpent, dest))

                            dest.setQ(cur[1].getDist() + timeSpent)
                    else:
                        #It will do this instead.
                        heapq.heappush(pq, (cur[1].getDist() + timeSpent, dest))
                        dest.setQ(cur[1].getDist() + timeSpent)
        
        self.dest = target
        self.graph = graph
    
    def getPath(self):
        #If the node has been visited, there's a valid path, so get the path object.
        if not self.dest.visited():
            return (False, 0)
        p = Path()
        p.fromDSP(self, self.dest)
        return True, p
