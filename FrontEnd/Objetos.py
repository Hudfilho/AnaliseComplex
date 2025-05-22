import pygame as pg

pg.font.init()
fonte = pg.font.Font(None, 70)
fonteP = pg.font.Font(None, 40)

class Botao():
    def __init__(self, x, y, sprite, spriteHover, emClick, tipoRender = False):
        self.sprite = sprite
        self.spriteHover = spriteHover
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        self.emClick = emClick
        self.click = True
        self.hover = False
        self.tipoRender = tipoRender

    def update(self, mouse_pos, mouseData):
        if not mouseData:
            self.click = True
        if self.rect.collidepoint(mouse_pos):
            self.hover = True
            if mouseData and self.click:
                self.emClick()
                self.click = False
        else:
            self.hover = False

    def render(self, tela):
        if self.hover:
            if self.tipoRender:
                tela.blit(self.sprite, (self.rect.x, self.rect.y))
            tela.blit(self.spriteHover, (self.rect.x, self.rect.y))
        else:
            tela.blit(self.sprite, (self.rect.x, self.rect.y))

class Botao2():
    def __init__(self, x, y, sprite, spriteClick, imgFundo, emClick, id, tipoRender = False):
        self.botao = Botao(x, y, sprite, sprite, self.switch, tipoRender)
        self.spriteClick = spriteClick
        self.sprite = sprite
        self.clicked = False
        self.emClick = emClick
        self.imgFundo = imgFundo
        self.imgFundoRect = self.imgFundo.get_rect()
        self.imgFundoRect.center = (x, y)
        self.id = id

    def switch(self):
        self.clicked = not self.clicked
        if self.clicked:
            self.botao.sprite = self.spriteClick
        else:
            self.botao.sprite = self.sprite
        self.emClick(self.id)

    def off(self):
        self.clicked = False
        self.botao.sprite = self.sprite
        self.botao.spriteHover = self.sprite

    def on(self):
        self.clicked = True
        self.botao.sprite = self.spriteClick
        self.botao.spriteHover = self.spriteClick

    def update(self, mouse_pos, mouseData):
        self.botao.update(mouse_pos, mouseData)
    
    def render(self, tela):
        if self.clicked:
            tela.blit(self.imgFundo, (self.imgFundoRect.x, self.imgFundoRect.y))
        self.botao.render(tela)

NodeIndexCount = 0
def resetNodeIndexCount():
    global NodeIndexCount
    NodeIndexCount = 0

class XY():
    def __init__(self, val):
        self.coords = val

nodeSprite = None
nodeSpriteHover = None
def setNodeSprite(sprite, spriteHover):
    global nodeSprite, nodeSpriteHover, nodeRadiusSqr
    nodeSprite = sprite
    nodeSpriteHover = spriteHover
    nodeRadiusSqr = (nodeSprite.get_width() // 2) ** 2

class Node():
    def __init__(self, xy):
        global NodeIndexCount, nodeSprite
        self.xy = XY(xy)
        self.hover = False
        self.click = False
        self.ativo = False
        self.rect = nodeSprite.get_rect()
        self.rect.center = xy
        self.id = NodeIndexCount
        self.texto = Texto(xy[0] - 20, xy[1] - 20, str(NodeIndexCount), fonte, (0,0,0))
        self.texto.rect.center = xy
        self.info = Texto(xy[0] - 20, xy[1] - 20, "", fonteP, (255,255,255))
        self.infoAtivo = False
        NodeIndexCount += 1

    def collide(self, mouse_pos, distSqr=2353):
        x1, y1 = mouse_pos
        return ((self.xy.coords[0] - x1)**2 + (self.xy.coords[1] - y1)**2) < distSqr
    
    def mover(self, xy):
        self.xy.coords = xy
        self.texto.xy = (xy[0] - 20, xy[1] - 20)
        self.texto.rect.center = xy
        self.rect.center = xy
        self.info.rect.bottomleft = (self.rect.topright[0] - 10, self.rect.topright[1] + 30)

    def update(self, mouse_pos, mouseData):
        if self.collide(mouse_pos):
            self.hover = True
            if mouseData and not self.click:
                self.click = True
                self.ativo = not self.ativo
        else:
            self.hover = False
            if not mouseData:
                self.click = False

    def setInfo(self, texto):
        self.info.setTextoNode(texto, self.rect.topleft)
        self.info.rect.bottomleft = (self.rect.topright[0] - 10, self.rect.topright[1] + 30)
        self.infoAtivo = True

    def render(self, tela):
        global nodeSprite, nodeSpriteHover
        if self.hover:
            tela.blit(nodeSpriteHover, (self.rect.x, self.rect.y))
        else:
            tela.blit(nodeSprite, (self.rect.x, self.rect.y))
        if self.infoAtivo:
            pg.draw.rect(tela, (18,12,34,100), (self.info.rect.x - 5, self.info.rect.y - 5, self.info.rect.width + 10, self.info.rect.height + 10))
            self.info.render(tela)
        self.texto.render(tela)

class Linha():
    def __init__(self, xy1, xy2):
        self.ponto0 = xy1
        self.ponto1 = xy2

    def render(self, tela):
        pg.draw.line(tela, (255, 255, 255), self.ponto0.coords , self.ponto1.coords, 10)

class Texto():
    def __init__(self, x, y, texto, f, cor=(255,255,255)):
        self.fonte = f
        self.textoSprite = self.fonte.render(texto, True, cor)
        self.rect = self.textoSprite.get_rect(topleft=(x, y))

    def update(self, mouse_pos, mouseData):
        if self.rect.collidepoint(mouse_pos) and mouseData:
            self.rect.center = (mouse_pos[0], mouse_pos[1])
            print(self.rect.center)

    def setTexto(self, novoTexto, w, cor=False):
        if cor:
            self.textoSprite = self.fonte.render(novoTexto, True, (221,25,29))
        else:
            self.textoSprite = self.fonte.render(novoTexto, True, (238,238,238))

        self.rect = self.textoSprite.get_rect(centerx=w // 2, y=self.rect.y)
        self.xy = (self.rect.x, self.rect.y)

    def setTextoNode(self, novoTexto, anchor):
        self.textoSprite = self.fonte.render(novoTexto, True, (238,238,238))
        self.rect = self.textoSprite.get_rect()
        self.rect.bottomleft = (anchor[0], anchor[1])

    def render(self, tela):
        tela.blit(self.textoSprite, self.rect.topleft)
        