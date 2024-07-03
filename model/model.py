import copy

import networkx as nx
from geopy import distance
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo= nx.Graph()
        self.idMap={}
        self.maxDistanza=0
        self.bestSol=[]



    def searchPath(self):

        parziale=[]
        self.maxDistanza=0
        for n in self._grafo.nodes():
            pesi=[0]
            archi_visitati=[]
            parziale=[n]
            self.ricorsione(parziale, pesi, archi_visitati)

    def ricorsione(self,parziale, pesi, archi_visitati):
        last=parziale[-1]
        vicini= sorted(self._grafo[last], key=lambda x: self._grafo[last][x]['weight'] )

        vicini_utilizzabili= []
        for v in vicini:
            if (last,v) not in archi_visitati and self._grafo[last][v]['weight'] > max(pesi):
                vicini_utilizzabili.append(v)

        if len(vicini_utilizzabili)==0:
            distanza=self.trovaDistanza(parziale)
            if distanza>self.maxDistanza:
                self.maxDistanza= distanza
                self.bestSol = copy.deepcopy(parziale)
            return

        for v in vicini_utilizzabili :
            pesi.append(self._grafo[last][v]['weight'])
            archi_visitati.append((last,v))
            parziale.append(v)

            self.ricorsione(parziale, pesi, archi_visitati)

            pesi.pop()
            archi_visitati.pop()
            parziale.pop()

    def trovaDistanza(self, parziale):
        distanza = 0.0
        for i  in range(len(parziale)-1):
            v1 = self.idMap[parziale[i]]
            v2 = self.idMap[parziale[i+1]]
            distanza += distance.geodesic((v1.Lat, v1.Lng), (v2.Lat, v2.Lng)).km
        return distanza




    def buildGraph(self, anno, forma):
        self._grafo.clear()
        brontolo = DAO.getNodi()
        nodi = []
        for n in brontolo:
            nodi.append(n.id)
            self.idMap[n.id] = n
        print(self.idMap)
        self._grafo.add_nodes_from(nodi)
        #self.idMap=DAO.getEdges()
        # for id in self.idMap:
        #     self._grafo.add_edge(id[0],id[1])
        self._grafo.add_weighted_edges_from(DAO.getPeso(anno, forma))


    def getPesoArco(self):
        pp=[]
        for n in self._grafo.nodes():
            somma=0
            for e in self._grafo.edges(n, data=True):
                somma+=e[2]['weight']
            pp.append((n, somma))
        return pp



    def getNodes(self):
        return len(self._grafo.nodes())

    def getEdges(self):
        return len(self._grafo.edges())



    def getAnni(self):
        return DAO.getYear()

    def getForma(self, anno):
        return DAO.getShape(anno)