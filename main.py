import pygame as pg
import FrontEnd.Objetos as obj
import BackEnd
import os
import sys

TELA_W = 1200
TELA_H = 1140

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

    textoMode = obj.Texto(0, 0, "", fonteM, (255, 255, 255))
    textoMode.setTexto("Add Node", TELA_W)

    nodes = []
    linhas = []

    def DFSClick():
        info = BackEnd.DFS()
        for node in nodes:
            node.setInfo(str(info[node.id]))
    def BFSClick():
        info = BackEnd.BFS()
        for node in nodes:
            node.setInfo(str(info[node.id]))
    btnBFS = obj.Botao(120, 453, img("BFS"), img("BFSHover"), BFSClick)
    btnDFS = obj.Botao(120, 550, img("DFS"), img("DFSHover"), DFSClick)
    
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

    btnSair = obj.Botao(1145,51,img("Sair"),img("SairHover"), sair, True)
    def btnClearClick():
        nonlocal nodes, linhas
        nodes = []
        linhas = []
        obj.resetNodeIndexCount()
    btnClear = obj.Botao(130,1075,img("Limpar"),img("LimparHover"), btnClearClick, True)
    mouse_pos = pg.mouse.get_pos()

    btns = [btnSair, btnClear, btnBFS, btnDFS, btnAddNode, btnAddLinha, btnMoverNode]

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

    def addNodeClick():
        for node in nodes:
            if node.collide(mouse_pos, 21500):
                return
        n = obj.Node(mouse_pos)
        n.setInfo("°")
        n.mover(mouse_pos)
        nodes.append(n)
        BackEnd.addNode(n.id)
    addNode[CLICK] = addNodeClick

    def addLinhaClick():
        nonlocal linhaAtiva, linhaNode0
        for node in nodes:
            if node.collide(mouse_pos):
                linhaNode0 = node
                linhaAtiva = True
                break
    def addLinhaHold():
        if linhaAtiva and linhaNode0 is not None:
            pg.draw.line(tela, (255, 255, 255), linhaNode0.xy.coords, mouse_pos, 10)
    def addLinhaRelease():
        nonlocal linhaAtiva, linhaNode0
        linhaAtiva = False
        for node in nodes:
            if node.collide(mouse_pos) and linhaNode0 is not None and node.xy.coords != linhaNode0.xy.coords:
                linhas.append(obj.Linha(linhaNode0.xy, node.xy))
                print("Linha adicionada " + str(linhaNode0.id) + " " + str(node.id))
                BackEnd.addLinha(linhaNode0.id, node.id)
                break
        linhaNode0 = None
    addLinha[CLICK] = addLinhaClick
    addLinha[HOLD] = addLinhaHold
    addLinha[RELEASE] = addLinhaRelease

    nodeMover = None
    def moverNodeClick():
        nonlocal nodeMover
        for node in nodes:
            if node.collide(mouse_pos):
                nodeMover = node
    def moverNodeHold():
        nonlocal nodeMover
        if nodeMover is not None:
            nodeMover.mover(mouse_pos)
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
                elif e.key == pg.K_b:
                    BFSClick()
                elif e.key == pg.K_d:
                    DFSClick()
                elif e.key == pg.K_ESCAPE:
                    sair()
            elif e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    mouseClick = True
            elif e.type == pg.MOUSEBUTTONUP:
                if e.button == 1:
                    mouseRelease = True

        tela.fill((18,12,34))

        mouse_pos = pg.mouse.get_pos()
        mouseData = pg.mouse.get_pressed()[0]
        mouseHold = pg.mouse.get_pressed()[0]

        for rect in noInpRects:
            if rect.collidepoint(mouse_pos):
                mouseClick = False
                mouseHold = False
                mouseRelease = False
                break

        if mouseClick:
            execF(inp[CLICK])
            print(mouse_pos)
        if mouseHold:
            execF(inp[HOLD])
        if mouseRelease:
            execF(inp[RELEASE])
        
        for linha in linhas:
            linha.render(tela)

        for node in nodes:
            node.update(mouse_pos, mouseData)
            node.render(tela)

        tela.blit(toolBar, (30, 30))

        if renderOutline:
            for node in nodes:
                if node.collide(mouse_pos, 21500):
                    outlineRect = outline.get_rect()
                    outlineRect.center = mouse_pos
                    tela.blit(outline, outlineRect)
                    break

        for btn in btns:
            btn.update(mouse_pos, mouseData)
            btn.render(tela)

        textoMode.update(mouse_pos, mouseData)
        textoMode.render(tela)

        pg.display.update()

    pg.quit()

main()