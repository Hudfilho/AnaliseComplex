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


def encontrar_componentes():
    """
    Encontra todos os componentes conectados do grafo
    Retorna uma lista de listas, onde cada lista interna contém os IDs dos nós de um componente
    """
    visitados = set()
    componentes = []

    for node_id in nodes.keys():
        if node_id not in visitados:
            # Novo componente encontrado
            componente = []
            # DFS para encontrar todos os nós deste componente
            stack = [node_id]

            while stack:
                atual = stack.pop()
                if atual not in visitados:
                    visitados.add(atual)
                    componente.append(atual)
                    # Adiciona todos os vizinhos não visitados
                    for vizinho in nodes[atual].vizinhosID:
                        if vizinho not in visitados:
                            stack.append(vizinho)

            componentes.append(componente)

    return componentes


def BFS_componente(node_inicial):
    """
    Executa BFS em um componente específico, começando do node_inicial
    Retorna dicionário com as distâncias
    """
    info_componente = {}
    visitados = set()
    fila = [node_inicial]

    visitados.add(node_inicial)
    info_componente[node_inicial] = 0
    print(f"Node {node_inicial} visitada (componente)")

    while fila:
        atual = fila.pop(0)
        distancia_atual = info_componente[atual]

        # Visita todos os vizinhos
        for vizinho in nodes[atual].vizinhosID:
            if vizinho not in visitados:
                visitados.add(vizinho)
                info_componente[vizinho] = distancia_atual + 1
                fila.append(vizinho)
                print(f"Node {vizinho} visitada (distância {distancia_atual + 1})")

    return info_componente


def BFS():
    """
    Executa BFS em todos os componentes do grafo
    Cada componente terá suas próprias distâncias começando do 0
    """
    if not nodes:
        print("Nenhum nó encontrado")
        return {}

    info_total = {}
    componentes = encontrar_componentes()

    print(f"Encontrados {len(componentes)} componente(s)")

    for i, componente in enumerate(componentes):
        print(f"\nProcessando componente {i + 1}: {componente}")

        # Escolhe o primeiro nó do componente como inicial
        # Você pode modificar isso para escolher o nó com menor ID ou outro critério
        node_inicial = min(componente)  # Usa o nó com menor ID

        # Executa BFS neste componente
        info_componente = BFS_componente(node_inicial)

        # Adiciona as informações ao resultado total
        info_total.update(info_componente)

    print("BFS completo para todos os componentes")
    return info_total


def DFS():
    """
    Executa DFS em todos os componentes do grafo
    """
    if not nodes:
        print("Nenhum nó encontrado")
        return {}

    global visitados, info, count
    count = 1
    info = {}
    visitados = set()

    componentes = encontrar_componentes()
    print(f"Encontrados {len(componentes)} componente(s) para DFS")

    for i, componente in enumerate(componentes):
        print(f"\nProcessando componente DFS {i + 1}: {componente}")

        # Escolhe o primeiro nó do componente como inicial
        node_inicial = min(componente)

        if node_inicial not in visitados:
            DFS_recusivo(node_inicial)

    print("DFS completo para todos os componentes")
    return info


visitados = set()
info = {}
count = 0


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