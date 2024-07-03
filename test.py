from model.model import Model

mymodel= Model()

mymodel.buildGraph()

print(f"nodi: {mymodel.getNodes()}, archi:{mymodel.getEdges()}")