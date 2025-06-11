class Node:
    def __init__(self):
        self.vizinhosID = []


mainNodeId = -1
nodes = {}
grafo_direcionado = False  # Nova variável global


def setGrafoDirecionado(direcionado=True):
    """
    Define se o grafo é direcionado ou não
    """
    global grafo_direcionado
    grafo_direcionado = direcionado
    print(f"Grafo configurado como: {'Direcionado' if direcionado else 'Não-direcionado'}")


def addNode(id):
    global mainNodeId
    if mainNodeId == -1:
        mainNodeId = id
    nodes[id] = Node()


def addLinha(id0, id1):
    """
    Adiciona aresta entre dois nós
    Se grafo_direcionado = True: aresta vai de id0 -> id1
    Se grafo_direcionado = False: aresta bidirecional id0 <-> id1
    """
    if id0 not in nodes:
        print("Node " + str(id0) + " não encontrado")
        return
    if id1 not in nodes:
        print("Node " + str(id1) + " não encontrado")
        return

    # Adiciona a aresta de id0 para id1
    if id1 not in nodes[id0].vizinhosID:
        nodes[id0].vizinhosID.append(id1)
        nodes[id0].vizinhosID.sort()

    # Se não é direcionado, adiciona também de id1 para id0
    if not grafo_direcionado:
        if id0 not in nodes[id1].vizinhosID:
            nodes[id1].vizinhosID.append(id0)
            nodes[id1].vizinhosID.sort()

    tipo = "direcionada" if grafo_direcionado else "bidirecional"
    print(f"Aresta {tipo} adicionada: {id0} -> {id1}")


def clear():
    global mainNodeId
    mainNodeId = -1
    nodes.clear()


def encontrar_componentes():
    """
    Para grafos direcionados: encontra componentes fracamente conectados
    Para grafos não-direcionados: encontra componentes conectados
    """
    visitados = set()
    componentes = []

    for node_id in nodes.keys():
        if node_id not in visitados:
            # Novo componente encontrado
            componente = []
            stack = [node_id]

            while stack:
                atual = stack.pop()
                if atual not in visitados:
                    visitados.add(atual)
                    componente.append(atual)

                    # Para grafos direcionados, considera conexões em ambas as direções
                    # para encontrar componentes fracamente conectados
                    vizinhos_a_visitar = set()

                    # Adiciona vizinhos diretos (saída)
                    vizinhos_a_visitar.update(nodes[atual].vizinhosID)

                    # Se é direcionado, também considera arestas de entrada
                    if grafo_direcionado:
                        for outro_id, outro_node in nodes.items():
                            if atual in outro_node.vizinhosID:
                                vizinhos_a_visitar.add(outro_id)

                    # Adiciona vizinhos não visitados à pilha
                    for vizinho in vizinhos_a_visitar:
                        if vizinho not in visitados:
                            stack.append(vizinho)

            componentes.append(componente)

    return componentes


def BFS_componente(node_inicial):
    """
    Executa BFS em um componente específico, começando do node_inicial
    Para grafos direcionados, só segue as arestas na direção correta
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

        # Visita apenas os vizinhos diretos (seguindo a direção das arestas)
        for vizinho in nodes[atual].vizinhosID:
            if vizinho not in visitados:
                visitados.add(vizinho)
                info_componente[vizinho] = distancia_atual + 1
                fila.append(vizinho)
                print(f"Node {vizinho} visitada (distância {distancia_atual + 1})")

    return info_componente


def BFS():
    """
    Executa BFS respeitando a direção das arestas se for grafo direcionado
    """
    if not nodes:
        print("Nenhum nó encontrado")
        return {}

    info_total = {}

    if grafo_direcionado:
        # Para grafos direcionados, executa BFS de cada nó separadamente
        visitados_global = set()

        for node_id in sorted(nodes.keys()):
            if node_id not in visitados_global:
                print(f"\nExecutando BFS direcionado a partir do nó {node_id}")
                info_componente = BFS_componente(node_id)
                info_total.update(info_componente)
                visitados_global.update(info_componente.keys())

        # Para nós não alcançáveis por nenhum BFS, adiciona com valor 0
        for node_id in nodes.keys():
            if node_id not in info_total:
                info_total[node_id] = 0
                print(f"Nó {node_id} é isolado")
    else:
        # Para grafos não-direcionados, usa o método original
        componentes = encontrar_componentes()
        print(f"Encontrados {len(componentes)} componente(s)")

        for i, componente in enumerate(componentes):
            print(f"\nProcessando componente {i + 1}: {componente}")
            node_inicial = min(componente)
            info_componente = BFS_componente(node_inicial)
            info_total.update(info_componente)

    print("BFS completo")
    return info_total


def DFS():
    """
    Executa DFS respeitando a direção das arestas se for grafo direcionado
    """
    if not nodes:
        print("Nenhum nó encontrado")
        return {}

    global visitados, info, count
    count = 1
    info = {}
    visitados = set()

    if grafo_direcionado:
        # Para grafos direcionados, executa DFS de cada nó não visitado
        for node_id in sorted(nodes.keys()):
            if node_id not in visitados:
                print(f"\nExecutando DFS direcionado a partir do nó {node_id}")
                DFS_recusivo(node_id)
    else:
        # Para grafos não-direcionados, usa componentes
        componentes = encontrar_componentes()
        print(f"Encontrados {len(componentes)} componente(s) para DFS")

        for i, componente in enumerate(componentes):
            print(f"\nProcessando componente DFS {i + 1}: {componente}")
            node_inicial = min(componente)
            if node_inicial not in visitados:
                DFS_recusivo(node_inicial)

    print("DFS completo")
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

        # Visita apenas os vizinhos diretos (respeitando direção)
        for vID in nodes[id].vizinhosID:
            DFS_recusivo(vID)

        postvisit = count
        count += 1
        info[id] = (previsit, postvisit)