import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allTeams = []
        self._idMapTeams = {}
        self._bestPath = []
        self._bestObjVal = 0

    def buildGraph(self, year):
        self._grafo.clear()
        if len(self._allTeams) == 0:
            print("Lista squadre vuota")
            return

        self._grafo.add_nodes_from(self._allTeams)
        myEdges = list(itertools.combinations(self._allTeams, 2))
        # itertools.combinations per avere le combinazioni lunghe 2 da una lista (no ripetute perché grafo non diretto)
        # le permutazioni hanno le ripetizioni, le combinazioni no
        self._grafo.add_edges_from(myEdges)
        salariesOfTeams = DAO.getSalaryOfTeams(year, self._idMapTeams)  # è un dizionario
        for e in self._grafo.edges:  # e = tupla (nodoP, nodoA)
            self._grafo[e[0]][e[1]]["weight"] = salariesOfTeams[e[0]] + salariesOfTeams[e[1]]

        """for t1 in self._grafo.nodes:
            for t2 in self._grafo.nodes:
                if t1 != t2:
                    self._grafo.add_edge(t1, t2)"""

    def getSortedNeighbors(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._grafo[v0][v]["weight"]))
        viciniTuples.sort(key=lambda x: x[1], reverse=True)
        return viciniTuples

    def getyears(self):
        years = DAO.getAllYears()
        return years

    def getTeamsOfYear(self, anno):
        self._allTeams = DAO.getTeamsOfYear(anno)
        self._idMapTeams = {t.ID: t for t in self._allTeams}
        return self._allTeams

    def printGraphData(self):
        print(f"Grafo creato con {len(self._grafo.nodes)} nodi"
              f"e {len(self._grafo.edges)} archi")

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getPercorso(self, v0):
        self._bestPath = []
        self._bestObjVal = 0
        parziale = [v0]
        """for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()"""
        listaVicini = []
        for v in self._grafo.neighbors(parziale[-1]):
            edgeV = self._grafo[v0][v]["weight"]
            listaVicini.append((v, edgeV))
        listaVicini.sort(key=lambda x: x[1], reverse=True)

        parziale.append(listaVicini[0][0])
        self._ricorsioneV2(parziale)
        parziale.pop()
        return self._bestPath

    def _ricorsione(self, parziale):
        # verifico se soluzione migliore del best
        if self._getScore(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        for v in self._grafo.neighbors(parziale[-1]):
            edgeW = self._grafo[parziale[-1]][v]["weight"]
            if (v not in parziale and
                    self._grafo[parziale[-2]][parziale[-1]]["weight"] > edgeW):
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()
        # aggiungo e faccio ricorsione

    def _getScore(self, listOfNodes):
        score = 0
        if len(listOfNodes) == 1:
            return 0
        for i in range(len(listOfNodes) - 1):
            score += self._grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]

        return score

    def _ricorsioneV2(self, parziale):
        # verifico se soluzione migliore del best
        if self._getScore(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        listaVicini = []
        for v in self._grafo.neighbors(parziale[-1]):
            edgeV = self._grafo[parziale[-1]][v]["weight"]
            listaVicini.append((v, edgeV))
        listaVicini.sort(key=lambda x: x[1], reverse=True)

        for v1 in listaVicini:      # scorro la lista (pesi decrescenti, prendo prima il più grande)
            if (v1[0] not in parziale and
                    self._grafo[parziale[-2]][parziale[-1]]["weight"] >
                    v1[1]):
                parziale.append(v1[0])
                self._ricorsione(parziale)
                parziale.pop()
                return      # chiamo sempre il vicino che pesa di più che non è in parziale e che pesa di meno del precedente
                # aggiungo e faccio ricorsione
