import pygame as pg
import math

pg.font.init()
fonte = pg.font.Font(None, 70)
fonteP = pg.font.Font(None, 40)


class Botao():
    def __init__(self, x, y, sprite, spriteHover, emClick, tipoRender=False):
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
    def __init__(self, x, y, sprite, spriteClick, imgFundo, emClick, id, tipoRender=False):
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
        self.texto = Texto(xy[0] - 20, xy[1] - 20, str(NodeIndexCount), fonte, (0, 0, 0))
        self.texto.rect.center = xy
        self.info = Texto(xy[0] - 20, xy[1] - 20, "", fonteP, (255, 255, 255))
        self.infoAtivo = False
        NodeIndexCount += 1

    def collide(self, mouse_pos, distSqr=2353):
        x1, y1 = mouse_pos
        return ((self.xy.coords[0] - x1) ** 2 + (self.xy.coords[1] - y1) ** 2) < distSqr

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
            pg.draw.rect(tela, (18, 12, 34, 100), (
            self.info.rect.x - 5, self.info.rect.y - 5, self.info.rect.width + 10, self.info.rect.height + 10))
            self.info.render(tela)
        self.texto.render(tela)


class Linha():
    def __init__(self, xy1, xy2, direcionada=False):
        self.ponto0 = xy1
        self.ponto1 = xy2
        self.direcionada = direcionada
        self.curvatura = 0  # 0 = reta, positivo = curva direita, negativo = curva esquerda

    def verificar_linha_oposta(self, todas_linhas):
        """
        Verifica se existe uma linha na direção oposta e ajusta a curvatura
        """
        if not self.direcionada:
            return

        for linha in todas_linhas:
            if linha != self and linha.direcionada:
                # Verifica se é a mesma conexão na direção oposta
                if (linha.ponto0.coords == self.ponto1.coords and
                        linha.ponto1.coords == self.ponto0.coords):
                    # Encontrou linha oposta! Ajustar curvaturas
                    self.curvatura = 30  # Esta linha curva para a direita
                    linha.curvatura = -30  # Linha oposta curva para a esquerda
                    break

    def calcular_pontos_curva(self, inicio, fim, curvatura):
        """
        Calcula os pontos de uma curva entre início e fim
        curvatura: positivo = curva direita, negativo = curva esquerda
        """
        if curvatura == 0:
            # Linha reta
            return [inicio, fim]

        # Calcula o ponto médio
        meio_x = (inicio[0] + fim[0]) / 2
        meio_y = (inicio[1] + fim[1]) / 2

        # Calcula o vetor perpendicular para o deslocamento da curva
        dx = fim[0] - inicio[0]
        dy = fim[1] - inicio[1]
        comprimento = math.sqrt(dx * dx + dy * dy)

        if comprimento == 0:
            return [inicio, fim]

        # Vetor perpendicular normalizado
        perp_x = -dy / comprimento
        perp_y = dx / comprimento

        # Ponto de controle da curva
        controle_x = meio_x + perp_x * curvatura
        controle_y = meio_y + perp_y * curvatura

        # Gera pontos da curva Bézier quadrática
        pontos = []
        num_pontos = 20
        for i in range(num_pontos + 1):
            t = i / num_pontos

            # Fórmula da curva Bézier quadrática
            x = (1 - t) ** 2 * inicio[0] + 2 * (1 - t) * t * controle_x + t ** 2 * fim[0]
            y = (1 - t) ** 2 * inicio[1] + 2 * (1 - t) * t * controle_y + t ** 2 * fim[1]

            pontos.append((x, y))

        return pontos

    def desenhar_seta_curva(self, tela, inicio, fim, curvatura, cor=(255, 255, 255), espessura=10):
        """
        Desenha uma seta com curva
        """
        # Ajusta pontos para não sobrepor aos nós
        dx = fim[0] - inicio[0]
        dy = fim[1] - inicio[1]
        comprimento = math.sqrt(dx * dx + dy * dy)

        if comprimento < 10:
            return

        dx_norm = dx / comprimento
        dy_norm = dy / comprimento

        raio_no = 30
        inicio_ajustado = (
            inicio[0] + dx_norm * raio_no,
            inicio[1] + dy_norm * raio_no
        )
        fim_ajustado = (
            fim[0] - dx_norm * raio_no,
            fim[1] - dy_norm * raio_no
        )

        # Calcula os pontos da curva
        pontos_curva = self.calcular_pontos_curva(inicio_ajustado, fim_ajustado, curvatura)

        # Desenha a curva como uma série de linhas pequenas
        for i in range(len(pontos_curva) - 1):
            pg.draw.line(tela, cor, pontos_curva[i], pontos_curva[i + 1], espessura)

        # Desenha a ponta da seta no final da curva
        if len(pontos_curva) >= 2:
            ultimo_ponto = pontos_curva[-1]
            penultimo_ponto = pontos_curva[-2]

            # Calcula a direção da seta baseada nos últimos pontos da curva
            dx_seta = ultimo_ponto[0] - penultimo_ponto[0]
            dy_seta = ultimo_ponto[1] - penultimo_ponto[1]
            angulo = math.atan2(dy_seta, dx_seta)

            # Tamanho e ângulo da seta
            tamanho_seta = 25
            angulo_seta = math.pi / 6  # 30 graus

            # Pontos da ponta da seta
            x1 = ultimo_ponto[0] - tamanho_seta * math.cos(angulo - angulo_seta)
            y1 = ultimo_ponto[1] - tamanho_seta * math.sin(angulo - angulo_seta)

            x2 = ultimo_ponto[0] - tamanho_seta * math.cos(angulo + angulo_seta)
            y2 = ultimo_ponto[1] - tamanho_seta * math.sin(angulo + angulo_seta)

            # Desenha as linhas da ponta da seta
            pg.draw.line(tela, cor, ultimo_ponto, (x1, y1), espessura)
            pg.draw.line(tela, cor, ultimo_ponto, (x2, y2), espessura)

    def desenhar_seta(self, tela, inicio, fim, cor=(255, 255, 255), espessura=10):
        """
        Desenha uma seta reta (método original para compatibilidade)
        """
        # Desenha a linha principal primeiro
        pg.draw.line(tela, cor, inicio, fim, espessura)

        # Calcula a direção da linha
        dx = fim[0] - inicio[0]
        dy = fim[1] - inicio[1]
        comprimento = math.sqrt(dx * dx + dy * dy)

        if comprimento < 10:  # Linha muito curta
            return

        # Normaliza o vetor direção
        dx_norm = dx / comprimento
        dy_norm = dy / comprimento

        # Ajusta o ponto final para não sobrepor ao nó
        raio_no = 60
        fim_ajustado = (
            fim[0] - dx_norm * raio_no,
            fim[1] - dy_norm * raio_no
        )

        # Tamanho e ângulo da seta
        tamanho_seta = 25
        angulo = math.atan2(dy, dx)
        angulo_seta = math.pi / 6  # 30 graus

        # Pontos da ponta da seta
        x1 = fim_ajustado[0] - tamanho_seta * math.cos(angulo - angulo_seta)
        y1 = fim_ajustado[1] - tamanho_seta * math.sin(angulo - angulo_seta)

        x2 = fim_ajustado[0] - tamanho_seta * math.cos(angulo + angulo_seta)
        y2 = fim_ajustado[1] - tamanho_seta * math.sin(angulo + angulo_seta)

        # Desenha as linhas da ponta da seta
        pg.draw.line(tela, cor, fim_ajustado, (x1, y1), espessura)
        pg.draw.line(tela, cor, fim_ajustado, (x2, y2), espessura)

    def render(self, tela):
        if self.direcionada:
            if self.curvatura != 0:
                # Desenha seta com curva
                self.desenhar_seta_curva(tela, self.ponto0.coords, self.ponto1.coords, self.curvatura)
            else:
                # Desenha seta reta
                self.desenhar_seta(tela, self.ponto0.coords, self.ponto1.coords)
        else:
            # Linha normal sem seta
            pg.draw.line(tela, (255, 255, 255), self.ponto0.coords, self.ponto1.coords, 10)


class Texto():
    def __init__(self, x, y, texto, f, cor=(255, 255, 255)):
        self.fonte = f
        self.textoSprite = self.fonte.render(texto, True, cor)
        self.rect = self.textoSprite.get_rect(topleft=(x, y))

    def update(self, mouse_pos, mouseData):
        if self.rect.collidepoint(mouse_pos) and mouseData:
            self.rect.center = (mouse_pos[0], mouse_pos[1])
            print(self.rect.center)

    def setTexto(self, novoTexto, w, cor=False):
        if cor:
            self.textoSprite = self.fonte.render(novoTexto, True, (221, 25, 29))
        else:
            self.textoSprite = self.fonte.render(novoTexto, True, (238, 238, 238))

        self.rect = self.textoSprite.get_rect(centerx=w // 2, y=self.rect.y)
        self.xy = (self.rect.x, self.rect.y)

    def setTextoNode(self, novoTexto, anchor):
        self.textoSprite = self.fonte.render(novoTexto, True, (238, 238, 238))
        self.rect = self.textoSprite.get_rect()
        self.rect.bottomleft = (anchor[0], anchor[1])

    def render(self, tela):
        tela.blit(self.textoSprite, self.rect.topleft)