class Node:
    def __init__(self):
        self.vizinhosID = []

mainNodeId = -1
nodes = {}

def addNode(id):
    global mainNodeId
    if mainNodeId == -1:
        mainNodeId = id
    nodes[id] = Node()

def addLinha(id0, id1):
    if id0 not in nodes:
        print("Node " + str(id0) + " n encontrada")
        return
    if id1 not in nodes:
        print("Node " + str(id1) + " n encontrada")
        return
    nodes[id0].vizinhosID.append(id1)
    nodes[id0].vizinhosID.sort()
    nodes[id1].vizinhosID.append(id0)
    nodes[id1].vizinhosID.sort()

def clear():
    global mainNodeId
    mainNodeId = -1
    nodes.clear()

visitados = set()
info = {}
count = 0
def DFS():
    if mainNodeId == -1:
        print("Nenhum nó principal encontrado")
        return
    global visitados, info, count
    count = 1
    info = {}
    visitados = set()
    DFS_recusivo(mainNodeId)
    print("DFS completo")
    return info

def DFS_recusivo(id):
    global count, info
    if id not in visitados and id in nodes:
        previsit = count
        count += 1
        print("Node " + str(id) + " visitada")
        visitados.add(id)
        for vID in nodes[id].vizinhosID:
            DFS_recusivo(vID)
        postvisit = count
        count += 1
        info[id] = (previsit, postvisit)

def BFS():
    if mainNodeId == -1:
        print("Nenhum nó principal encontrado")
        return
    global visitados, count
    count = 0
    info = {}
    visitados = set()
    visitar = []
    visitar.extend(nodes[mainNodeId].vizinhosID)
    visitados.add(mainNodeId)
    print("Node " + str(mainNodeId) + " visitada")
    info[mainNodeId] = (0)
    while len(visitar) != 0:
        count += 1
        tmp = []
        for id in visitar:
            print("Node " + str(id) + " visitada")
            info[id] = count
            visitados.add(id)
            for vID in nodes[id].vizinhosID:
                if vID not in visitados and vID not in tmp and vID not in visitar:
                    tmp.append(vID)
        visitar = tmp
    print("BFS completo")
    return info
