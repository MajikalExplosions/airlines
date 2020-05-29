# Name: YenKSP.py
# Description: Finds the K shortest paths between two airports using Yen's algorithm.

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/23/20		Original

from flights.paths.DijkstraSP import DijkstraSP
from flights.paths.Path import Path

class YenKSP:

    def __init__(self, graph, origin, dest, ow=0):
        self.graph = graph
        self.origin = origin
        self.dest = dest
        self.k = 0
        self.A = []
        self.B = []
        self.hasNext = True
        self.w = ow

    def solve(self):
        self.graph.resetAll()
        if self.k == 0:
            validPath, _path = DijkstraSP(self.graph, self.origin, self.dest, rootVal=self.w).getPath()
            self.A = [_path]
            self.k = 1
            return True

        path = self.A[-1]
        for i in range(len(self.A[-1].getNodes()) - 2, -1, -1):
            rootPath = path.sliceToPath(0, i)
        
            #Remove edges that have already been traveled on starting at spur node
            removedEdges = []
            for p2 in self.A:
                if rootPath.equals(p2.sliceToPath(0, i)):
                    removedEdges.append(p2.getEdges()[i])

            #Find the spur path
            spurNode = rootPath.getNodes()[i]

            #You can't reset the nodes along the root path, for obvious reasons.
            self.graph.removeEdges(removedEdges)
            self.graph.reset(rootPath)

            #Search for an alternate path starting from the spur node
            validPath, spurPath = DijkstraSP(self.graph, spurNode, self.dest, rootVal=rootPath.getDists()[-1] + self.w).getPath()
            self.graph.addEdges(removedEdges)

            if not validPath:
                print("No valid paths")
                continue
            
            #If there is a valid path, combine it with the root path to the spur node
            totalPath = Path()
            totalPath.fromTwo(rootPath, spurPath)

            #Add it to B
            inB = False
            for p2 in self.B:
                if p2.equals(totalPath):
                    inB = True
            
            if not inB:
                self.B.append(totalPath)

        
        if len(self.B) == 0:
            self.hasNext = False
            return False

        #The shortest path in B is guaranteed to be the next shortest possible path, so move that to A.
        self.B.sort(key=yksp_pathLength)
        self.A.append(self.B[0])
        self.B = self.B[1:]
        
        #Reset graph
        self.graph.resetAll()
        self.k += 1
        return True
    
    def getPath(self, k):
        for k2 in range(self.k, k + 1):
            if not self.hasNext:
                return "No other paths."
            found = self.solve()
            if not found:
                return "No other paths."
            
        return self.A[k]



def yksp_pathLength(path):
    #Get the distance to the dest for each path
    path.recalculateDist(0)
    return path.getDists()[-1]