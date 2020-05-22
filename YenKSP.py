# Name: YenKSP.py
# Description: Finds the K shortest paths between two airports using a modified Eppstein's KSP algorithm optimized for small values of K.

# Ver.	Writer			        Date			Notes
# 1.0   Joseph Liu              05/15/20		Original

from DijkstraSP import *

class YenKSP:
    def __init__(self, graph, origin, dest, k):
        A = [DijkstraSP(graph, origin).getPathNode(dest)]
        B = []

        for pathNum in range(1, k):
            pathNodes = A[pathNum - 1]

            for i in range(len(A[pathNum - 1]) - 1):
                spurNode = pathNodes[i]
                rootPath = pathNodes[:i + 1]
            
                removedEdges = []
                removedNodes = []
                for path in A:
                    if rootPath == path.getPathNode(dest)[:i + 1]:
                        removedEdges.append(graph.getNodes()[i + 1].getEdgeIn())
                
                graph.removeEdges(removedEdges)
                
                for node in rootPath[:-1]:
                    removedNodes.append(node)
                
                graph.removeNodes(removedNodes)

                spurPath = DijkstraSP(graph, spurNode)
                
                totalPath = rootPath + spurPath
                if totalPath not in B:
                    B.append(totalPath)
                
                graph.addNodes(removedNodes)
                graph.addEdges(removedEdges)

                if len(B) == 0:
                    break

                B.sort(key=pathLength)
                A.append(B[0])
                B = B[1:]
        
        self.paths = A
    
    def getPath(self, k):
        return self.paths[k]

    def pathLength(a):
        return a[-1].getDist()