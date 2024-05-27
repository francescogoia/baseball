import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allTeams = []


    def buildGraph(self):
        self._grafo.clear()
        if len(self._allTeams) == 0:
            print("Lista squadre vuota")
            return

        self._grafo.add_nodes_from(self._allTeams)
        myEdges = list(itertools.combinations(self._allTeams, 2))
        # itertools.combinations per avere le combinazioni lunghe 2 da una lista (no ripetute)
        # le permutazioni hanno le ripetizioni, le combinazioni no
        self._grafo.add_edges_from(myEdges)
        """for t1 in self._grafo.nodes:
            for t2 in self._grafo.nodes:
                if t1 != t2:
                    self._grafo.add_edge(t1, t2)"""

    def getyears(self):
        years = DAO.getAllYears()
        return years

    def getTeamsOfYear(self, anno):
        self._allTeams = DAO.getTeamsOfYear(anno)
        return self._allTeams

    def printGraphData(self):
        print(f"Grafo creato con {len(self._grafo.nodes)} nodi"
              f"e {len(self._grafo.edges)} archi")