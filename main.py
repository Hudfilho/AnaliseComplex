import pygame as pg
import FrontEnd.Objetos as obj
import BackEnd
import os
import sys

TELA_W = 1200 * 0.8
TELA_H = 1140 * 0.8

FPS = 60

CLICK = 0
HOLD = 1
RELEASE = 2

pg.init()

path = "FrontEnd/img/"
tela = pg.display.set_mode((TELA_W, TELA_H))
fonteP = pg.font.Font(None, 40)
fonteM = pg.font.Font(None, 70)
fonteG = pg.font.Font(None, 110)
pg.display.set_caption("Graficos")

inputOp = []
textoOp = []


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def img(s: str, tipo="png"):
    path = resource_path(f"FrontEnd/img/{s}.{tipo}")
    return pg.image.load(path).convert_alpha()


def execF(f):
    if callable(f):
        f()


def sair():
    print("Saindo...")
    global cont
    cont = False


pg.display.set_icon(img("mage", "jpg"))

cont = True


def main():
    global cont
    clock = pg.time.Clock()

    # Inicializa a câmera
    obj.init_camera(TELA_W, TELA_H)

    textoMode = obj.Texto(0, 0, "", fonteM, (255, 255, 255))
    textoMode.setTexto("Add Node", TELA_W)

    # Texto para mostrar o tipo de grafo
    textoTipoGrafo = obj.Texto(10, 10, "Grafo: Não-direcionado", fonteP, (255, 255, 0))

    # Texto para mostrar informações do zoom
    textoZoom = obj.Texto(10, 50, f"Zoom: {obj.camera.zoom:.2f}x", fonteP, (200, 200, 255))

    nodes = []
    linhas = []

    def DFSClick():
        info = BackEnd.DFS()
        for node in nodes:
            if node.id in info:
                node.setInfo(str(info[node.id]))
            else:
                node.setInfo("∞")

    def BFSClick():
        info = BackEnd.BFS()
        for node in nodes:
            if node.id in info:
                node.setInfo(str(info[node.id]))
            else:
                node.setInfo("∞")  # Indica nó não alcançável

    def toggleGrafoDirecionado():
        """
        Alterna entre grafo direcionado e não-direcionado
        """
        BackEnd.setGrafoDirecionado(not BackEnd.grafo_direcionado)

        # Atualiza o texto indicativo
        if BackEnd.grafo_direcionado:
            textoTipoGrafo.textoSprite = textoTipoGrafo.fonte.render("Grafo: Direcionado", True, (255, 100, 100))
            print("Modo: Grafo Direcionado - Arestas terão direção!")
        else:
            textoTipoGrafo.textoSprite = textoTipoGrafo.fonte.render("Grafo: Não-direcionado", True, (100, 255, 100))
            print("Modo: Grafo Não-direcionado - Arestas bidirecionais")

        # Debug: verificar linhas existentes
        print(f"Linhas existentes: {len(linhas)}")
        for i, linha in enumerate(linhas):
            print(f"Linha {i}: direcionada = {linha.direcionada}")

    def debugLinhas():
        """
        Função para debugar as linhas criadas
        """
        print(f"\n--- DEBUG LINHAS ---")
        print(f"Total de linhas: {len(linhas)}")
        print(f"Grafo direcionado: {BackEnd.grafo_direcionado}")
        for i, linha in enumerate(linhas):
            print(f"Linha {i}: {linha.ponto0.coords} -> {linha.ponto1.coords}, direcionada: {linha.direcionada}")
        print("--- FIM DEBUG ---\n")

    def resetZoom():
        """Reset zoom e posição da câmera"""
        obj.camera.zoom = 1.0
        obj.camera.x = 0
        obj.camera.y = 0
        print("Zoom resetado!")

    btnBFS = obj.Botao(120, 453, img("BFS"), img("BFSHover"), BFSClick)
    btnDFS = obj.Botao(120, 550, img("DFS"), img("DFSHover"), DFSClick)

    # Botão para alternar tipo de grafo - crie uma imagem simples ou use texto
    btnDirecionado = obj.Botao(120, 647, img("Node"), img("NodeHover"), toggleGrafoDirecionado)

    def switchMode(mode):
        nonlocal inp, btnAddNode, btnAddLinha, btnMoverNode, renderOutline
        if mode == 0:
            btnAddNode.on()
            btnAddLinha.off()
            btnMoverNode.off()
            inp = addNode
            textoMode.setTexto("Add Node", TELA_W)
            renderOutline = True
        elif mode == 1:
            btnAddNode.off()
            btnAddLinha.on()
            btnMoverNode.off()
            inp = addLinha
            textoMode.setTexto("Add Linha", TELA_W)
            renderOutline = False
        elif mode == 2:
            btnAddNode.off()
            btnAddLinha.off()
            btnMoverNode.on()
            inp = moverNode
            textoMode.setTexto("Mover Node", TELA_W)
            renderOutline = False

    obj.setNodeSprite(img("Node"), img("NodeHover"))
    imgClickFundo = img("QuadradoBranco")
    btnAddNode = obj.Botao2(85, 85, img("AddNode"), img("AddNodeClick"), imgClickFundo, switchMode, 0, False)
    btnAddLinha = obj.Botao2(85, 209, img("AddLinha"), img("AddLinhaClick"), imgClickFundo, switchMode, 1, True)
    btnMoverNode = obj.Botao2(85, 330, img("MoverNode"), img("MoverNodeClick"), imgClickFundo, switchMode, 2, True)

    toolBar = img("ToolBar")

    btnSair = obj.Botao(1145, 51, img("Sair"), img("SairHover"), sair, True)

    def btnClearClick():
        nonlocal nodes, linhas
        nodes = []
        linhas = []
        obj.resetNodeIndexCount()
        BackEnd.clear()

    def btnResetClick():
        """Reset completo da aplicação"""
        nonlocal nodes, linhas, inp, renderOutline
        # Limpa todos os dados
        nodes = []
        linhas = []
        obj.resetNodeIndexCount()
        BackEnd.clear()

        # Reset da câmera
        obj.camera.zoom = 1.0
        obj.camera.x = 0
        obj.camera.y = 0

        # Reset para modo padrão (Add Node)
        switchMode(0)

        # Reset tipo de grafo para não-direcionado
        BackEnd.setGrafoDirecionado(False)
        textoTipoGrafo.textoSprite = textoTipoGrafo.fonte.render("Grafo: Não-direcionado", True, (100, 255, 100))

        print("Aplicação reiniciada!")

    btnClear = obj.Botao(130, 1075, img("Limpar"), img("LimparHover"), btnClearClick, True)
    btnReset = obj.Botao(230, 1075, img("Node"), img("NodeHover"), btnResetClick,
                         True)  # Usando img Node temporariamente
    mouse_pos = pg.mouse.get_pos()

    btns = [btnSair, btnClear, btnReset, btnBFS, btnDFS, btnDirecionado, btnAddNode, btnAddLinha, btnMoverNode]

    mouseHold = False
    mouseRelease = False
    mouseClick = False

    linhaAtiva = False
    linhaNode0 = None

    addNode = [None, None, None]
    addLinha = [None, None, None]
    moverNode = [None, None, None]

    noInpRects = [pg.Rect(0, 0, 230, 596)]

    outline = img("Outline")
    renderOutline = False

    # Variáveis para pan da câmera
    panning = False
    last_pan_pos = (0, 0)

    def addNodeClick():
        world_mouse_pos = obj.camera.screen_to_world(mouse_pos)
        for node in nodes:
            if node.collide(world_mouse_pos, 21500):
                return
        n = obj.Node(world_mouse_pos)
        n.setInfo("°")
        n.mover(world_mouse_pos)
        nodes.append(n)
        BackEnd.addNode(n.id)

    addNode[CLICK] = addNodeClick

    def addLinhaClick():
        nonlocal linhaAtiva, linhaNode0
        world_mouse_pos = obj.camera.screen_to_world(mouse_pos)
        for node in nodes:
            if node.collide(world_mouse_pos):
                linhaNode0 = node
                linhaAtiva = True
                break

    def addLinhaHold():
        if linhaAtiva and linhaNode0 is not None:
            # Mostra uma prévia da linha/seta sendo criada
            world_mouse_pos = obj.camera.screen_to_world(mouse_pos)
            inicio_screen = obj.camera.world_to_screen(linhaNode0.xy.coords)
            fim_screen = mouse_pos  # Usa a posição do mouse na tela diretamente

            if BackEnd.grafo_direcionado:
                # Desenha uma seta temporária
                pg.draw.line(tela, (150, 150, 150), inicio_screen, fim_screen, max(1, int(5 * obj.camera.zoom)))

                # Desenha uma seta simples no final
                import math
                dx = fim_screen[0] - inicio_screen[0]
                dy = fim_screen[1] - inicio_screen[1]
                if dx != 0 or dy != 0:
                    angulo = math.atan2(dy, dx)
                    tamanho_seta = 15 * obj.camera.zoom
                    angulo_seta = math.pi / 6

                    x1 = fim_screen[0] - tamanho_seta * math.cos(angulo - angulo_seta)
                    y1 = fim_screen[1] - tamanho_seta * math.sin(angulo - angulo_seta)
                    x2 = fim_screen[0] - tamanho_seta * math.cos(angulo + angulo_seta)
                    y2 = fim_screen[1] - tamanho_seta * math.sin(angulo + angulo_seta)

                    espessura = max(1, int(5 * obj.camera.zoom))
                    pg.draw.line(tela, (150, 150, 150), fim_screen, (x1, y1), espessura)
                    pg.draw.line(tela, (150, 150, 150), fim_screen, (x2, y2), espessura)
            else:
                pg.draw.line(tela, (150, 150, 150), inicio_screen, fim_screen, max(1, int(5 * obj.camera.zoom)))

    def addLinhaRelease():
        nonlocal linhaAtiva, linhaNode0
        linhaAtiva = False
        world_mouse_pos = obj.camera.screen_to_world(mouse_pos)
        for node in nodes:
            if node.collide(world_mouse_pos) and linhaNode0 is not None and node.xy.coords != linhaNode0.xy.coords:
                # Cria linha direcionada ou não baseado no tipo de grafo
                linha = obj.Linha(linhaNode0.xy, node.xy, BackEnd.grafo_direcionado)
                linhas.append(linha)

                if BackEnd.grafo_direcionado:
                    print(f"Aresta direcionada adicionada: {linhaNode0.id} -> {node.id}")
                else:
                    print(f"Aresta adicionada: {linhaNode0.id} <-> {node.id}")

                BackEnd.addLinha(linhaNode0.id, node.id)
                break
        linhaNode0 = None

    addLinha[CLICK] = addLinhaClick
    addLinha[HOLD] = addLinhaHold
    addLinha[RELEASE] = addLinhaRelease

    nodeMover = None

    def moverNodeClick():
        nonlocal nodeMover
        world_mouse_pos = obj.camera.screen_to_world(mouse_pos)
        for node in nodes:
            if node.collide(world_mouse_pos):
                nodeMover = node

    def moverNodeHold():
        nonlocal nodeMover
        if nodeMover is not None:
            world_mouse_pos = obj.camera.screen_to_world(mouse_pos)
            nodeMover.mover(world_mouse_pos)

    def moverNodeRelease():
        nonlocal nodeMover
        nodeMover = None

    moverNode[CLICK] = moverNodeClick
    moverNode[HOLD] = moverNodeHold
    moverNode[RELEASE] = moverNodeRelease

    inp = addNode
    switchMode(0)

    while cont:
        dt = clock.tick(FPS)
        mouseHold = False
        mouseRelease = False
        mouseClick = False

        for e in pg.event.get():
            if e.type == pg.QUIT:
                cont = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_1:
                    switchMode(0)
                elif e.key == pg.K_2:
                    switchMode(1)
                elif e.key == pg.K_3:
                    switchMode(2)
                elif e.key == pg.K_4:
                    btnClearClick()
                elif e.key == pg.K_5:  # Nova tecla para reset completo
                    btnResetClick()
                elif e.key == pg.K_b:
                    BFSClick()
                elif e.key == pg.K_d:
                    DFSClick()
                elif e.key == pg.K_g:  # Nova tecla para alternar grafo direcionado
                    toggleGrafoDirecionado()
                elif e.key == pg.K_l:  # Nova tecla para debug das linhas
                    debugLinhas()
                elif e.key == pg.K_r:  # Nova tecla para resetar zoom
                    resetZoom()
                elif e.key == pg.K_ESCAPE:
                    sair()
                # Controles de zoom por teclado
                elif e.key == pg.K_PLUS or e.key == pg.K_EQUALS:
                    obj.camera.zoom_at(mouse_pos, 1.2)
                elif e.key == pg.K_MINUS:
                    obj.camera.zoom_at(mouse_pos, 0.8)
            elif e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:  # Botão esquerdo
                    mouseClick = True
                elif e.button == 2:  # Botão do meio - pan
                    panning = True
                    last_pan_pos = mouse_pos
                elif e.button == 3:  # Botão direito - também pan
                    panning = True
                    last_pan_pos = mouse_pos
            elif e.type == pg.MOUSEBUTTONUP:
                if e.button == 1:
                    mouseRelease = True
                elif e.button == 2 or e.button == 3:
                    panning = False
            elif e.type == pg.MOUSEWHEEL:
                # Zoom com roda do mouse
                if e.y > 0:  # Scroll up - zoom in
                    obj.camera.zoom_at(mouse_pos, 1.1)
                elif e.y < 0:  # Scroll down - zoom out
                    obj.camera.zoom_at(mouse_pos, 0.9)

        tela.fill((18, 12, 34))

        mouse_pos = pg.mouse.get_pos()
        mouseData = pg.mouse.get_pressed()[0]
        mouseHold = pg.mouse.get_pressed()[0]

        # Handle panning
        if panning:
            current_pos = mouse_pos
            dx = current_pos[0] - last_pan_pos[0]
            dy = current_pos[1] - last_pan_pos[1]
            obj.camera.move(-dx, -dy)
            last_pan_pos = current_pos

        # Verifica se o mouse está sobre a toolbar para desabilitar input
        for rect in noInpRects:
            if rect.collidepoint(mouse_pos):
                mouseClick = False
                mouseHold = False
                mouseRelease = False
                panning = False  # Também desabilita pan sobre a toolbar
                break

        # Converte posição do mouse para coordenadas do mundo
        world_mouse_pos = obj.camera.screen_to_world(mouse_pos)

        if mouseClick:
            execF(inp[CLICK])
            print(f"Screen: {mouse_pos}, World: {world_mouse_pos}")
        if mouseHold and not panning:
            execF(inp[HOLD])
        if mouseRelease:
            execF(inp[RELEASE])

        # Renderiza linhas primeiro (para ficarem atrás dos nós)
        for linha in linhas:
            linha.render(tela)

        # Renderiza nós
        for node in nodes:
            node.update(world_mouse_pos, mouseData)
            node.render(tela)

        # Renderiza UI (sempre por cima)
        tela.blit(toolBar, (30, 30))

        # Renderiza o texto do tipo de grafo
        textoTipoGrafo.render(tela)

        # Atualiza e renderiza texto do zoom
        textoZoom.textoSprite = textoZoom.fonte.render(f"Zoom: {obj.camera.zoom:.2f}x", True, (200, 200, 255))
        textoZoom.render(tela)

        # Renderiza outline para modo Add Node
        if renderOutline:
            for node in nodes:
                if node.collide(world_mouse_pos, 21500):
                    outlineRect = outline.get_rect()
                    outlineRect.center = mouse_pos
                    tela.blit(outline, outlineRect)
                    break

        # Renderiza botões
        for btn in btns:
            btn.update(mouse_pos, mouseData)
            btn.render(tela)

        # Renderiza texto do modo
        textoMode.update(mouse_pos, mouseData)
        textoMode.render(tela)

        # Renderiza instruções de controle na tela
        instrucoes = [
            "Controles:",
            "Roda do Mouse: Zoom",
            "Botão Meio/Direito: Pan",
            "+/- : Zoom por teclado",
            "R: Reset zoom",
            "G: Alternar grafo direcionado",
            "5: Reset completo da aplicação"
        ]

        y_offset = TELA_H - 150
        for i, instrucao in enumerate(instrucoes):
            texto_instrucao = fonteP.render(instrucao, True, (150, 150, 150) if i == 0 else (100, 100, 100))
            tela.blit(texto_instrucao, (10, y_offset + i * 20))

        pg.display.update()

    pg.quit()


main()