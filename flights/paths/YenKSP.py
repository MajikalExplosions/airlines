# Name: YenKSP.py
# Description: Finds the K shortest paths between two airports using Yen's algorithm

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/23/20		Original

from flights.paths.DijkstraSP import DijkstraSP
from flights.paths.Path import Path

class YenKSP:
    def __init__(self, graph, origin, dest, k, fm=0):
        graph.resetAll()
        validPath, _path = DijkstraSP(graph, origin).getPath(dest)
        A = [_path]
        B = []

        for pathNum in range(1, k):
            path = A[pathNum - 1]
            for i in range(len(A[pathNum - 1].getNodes()) - 2, -1, -1):
                rootPath = path.sliceToPath(0, i)
            
                #Remove edges that have already been traveled on starting at spur node
                removedEdges = []
                for p2 in A:
                    if rootPath.equals(p2.sliceToPath(0, i)):
                        removedEdges.append(p2.getEdges()[i])
                graph.removeEdges(removedEdges)

                #Find the spur path
                spurNode = rootPath.getNodes()[i]
                #You can't reset the nodes along the root path, for obvious reasons.
                
                graph.reset(rootPath)
                validPath, spurPath = DijkstraSP(graph, spurNode, rootVal=rootPath.getDists()[-1]).getPath(dest)

                if not validPath:
                    self.paths = A
                    graph.resetAll()
                    return
                
                totalPath = Path()
                totalPath.fromTwo(rootPath, spurPath)

                inB = False
                for p2 in B:
                    if p2.equals(totalPath):
                        inB = True
                
                if not inB:
                    B.append(totalPath)

                graph.addEdges(removedEdges)

                if len(B) == 0:
                    break
            B.sort(key=yksp_pathLength)
            A.append(B[0])
            B = B[1:]
        
        #Reset graph
        graph.resetAll()
        self.paths = A
    
    def getPath(self, k):
        return self.paths[k]

def yksp_pathLength(path):
    path.recalculateDist(0)
    return path.getDists()[-1]