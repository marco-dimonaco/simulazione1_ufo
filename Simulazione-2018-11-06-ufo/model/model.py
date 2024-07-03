import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}
        for i in DAO.getAllStates():
            self._idMap[i.id] = i

    def buildGraph(self, anno):
        self._grafo.clear()
        allNodes = DAO.getStates(anno)
        self._grafo.add_nodes_from(allNodes)
        self.addEdges(anno)
        return True

    def addEdges(self, anno):
        allConnessioni = DAO.getConnections(self._idMap, anno)
        for c in allConnessioni:
            self._grafo.add_edge(c.st1, c.st2)

    def getSuccessori(self, origine):
        successori = list(self._grafo.successors(self._idMap[origine]))
        return successori

    def getPredecessori(self, origine):
        predecessori = list(self._grafo.predecessors(self._idMap[origine]))
        return predecessori

    def getRaggiungibili(self, origine):
        raggiungibili = list(nx.dfs_tree(self._grafo, self._idMap[origine]))
        return raggiungibili, len(raggiungibili)

    @staticmethod
    def getYears():
        return DAO.getAllYears()

    def getNodes(self):
        return self._grafo.nodes

    def printGraphDetails(self):
        return (f"#Vertici: {len(self._grafo.nodes)}\n"
                f"#Archi: {len(self._grafo.edges)}")
