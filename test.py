from model.model import Model

myModel = Model()
myModel.getyears()
myModel.getTeamsOfYear(2015)
myModel.buildGraph(2015)
myModel.printGraphData()

v0 = list(myModel._grafo.nodes)[10]
vicini = myModel.getSortedNeighbors(v0)
"""for v in vicini:
    print(v[1], v[0])"""

path = myModel.getPercorso(v0)
print(len(path))
