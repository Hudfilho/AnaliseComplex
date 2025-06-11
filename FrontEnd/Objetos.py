import pygame as pg
import math

pg.font.init()
fonte = pg.font.Font(None, 70)
fonteP = pg.font.Font(None, 40)


class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 3.0
        self.width = width
        self.height = height

    def world_to_screen(self, world_pos):
        """Converte coordenadas do mundo para coordenadas da tela"""
        screen_x = (world_pos[0] - self.x) * self.zoom
        screen_y = (world_pos[1] - self.y) * self.zoom
        return (screen_x, screen_y)

    def screen_to_world(self, screen_pos):
        """Converte coordenadas da tela para coordenadas do mundo"""
        world_x = screen_pos[0] / self.zoom + self.x
        world_y = screen_pos[1] / self.zoom + self.y
        return (world_x, world_y)

    def zoom_at(self, screen_pos, zoom_delta):
        """Faz zoom mantendo o ponto da tela fixo"""
        # Converte posição da tela para mundo antes do zoom
        world_pos = self.screen_to_world(screen_pos)

        # Aplica o zoom
        old_zoom = self.zoom
        self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom * zoom_delta))

        # Se o zoom realmente mudou, ajusta a posição da câmera
        if self.zoom != old_zoom:
            # Converte de volta para mundo com novo zoom
            new_world_pos = self.screen_to_world(screen_pos)

            # Ajusta posição da câmera para manter o ponto fixo
            self.x += world_pos[0] - new_world_pos[0]
            self.y += world_pos[1] - new_world_pos[1]

    def move(self, dx, dy):
        """Move a câmera"""
        self.x += dx / self.zoom
        self.y += dy / self.zoom


# Instância global da câmera
camera = None


def init_camera(width, height):
    global camera
    camera = Camera(width, height)


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
        self.info_texto = ""  # Armazena o texto atual da info
        self.infoAtivo = False
        NodeIndexCount += 1

    def collide(self, world_mouse_pos, distSqr=2353):
        x1, y1 = world_mouse_pos
        return ((self.xy.coords[0] - x1) ** 2 + (self.xy.coords[1] - y1) ** 2) < distSqr

    def mover(self, xy):
        self.xy.coords = xy
        self.texto.xy = (xy[0] - 20, xy[1] - 20)
        self.texto.rect.center = xy
        self.rect.center = xy
        self.info.rect.bottomleft = (self.rect.topright[0] - 10, self.rect.topright[1] + 30)

    def update(self, world_mouse_pos, mouseData):
        if self.collide(world_mouse_pos):
            self.hover = True
            if mouseData and not self.click:
                self.click = True
                self.ativo = not self.ativo
        else:
            self.hover = False
            if not mouseData:
                self.click = False

    def setInfo(self, texto):
        # Armazena o texto atual para uso posterior
        self.info_texto = texto
        self.info.setTextoNode(texto, self.rect.topleft)
        self.info.rect.bottomleft = (self.rect.topright[0] - 10, self.rect.topright[1] + 30)
        self.infoAtivo = True

    def render(self, tela):
        global nodeSprite, nodeSpriteHover, camera
        if camera is None:
            return

        # Converte posição do mundo para tela
        screen_pos = camera.world_to_screen(self.xy.coords)

        # Calcula o tamanho do nó baseado no zoom
        scaled_width = int(nodeSprite.get_width() * camera.zoom)
        scaled_height = int(nodeSprite.get_height() * camera.zoom)

        # Só renderiza se estiver visível na tela
        if (-scaled_width < screen_pos[0] < camera.width and
                -scaled_height < screen_pos[1] < camera.height):

            # Escala o sprite do nó
            if self.hover:
                scaled_sprite = pg.transform.scale(nodeSpriteHover, (scaled_width, scaled_height))
            else:
                scaled_sprite = pg.transform.scale(nodeSprite, (scaled_width, scaled_height))

            # Centraliza o sprite
            sprite_rect = scaled_sprite.get_rect()
            sprite_rect.center = screen_pos
            tela.blit(scaled_sprite, sprite_rect)

            # Renderiza info se ativo
            if self.infoAtivo:
                # Posição da info na tela
                info_world_pos = (self.xy.coords[0] + 40, self.xy.coords[1] - 40)
                info_screen_pos = camera.world_to_screen(info_world_pos)

                # Renderiza o texto da info usando o texto armazenado
                info_surface = self.info.fonte.render(str(self.info_texto), True, (255, 255, 255))
                info_rect = info_surface.get_rect()
                info_rect.topleft = info_screen_pos

                # Fundo da info
                pg.draw.rect(tela, (18, 12, 34, 200),
                             (info_rect.x - 5, info_rect.y - 5,
                              info_rect.width + 10, info_rect.height + 10))
                tela.blit(info_surface, info_screen_pos)

            # Renderiza o texto do ID do nó
            texto_screen_pos = camera.world_to_screen(self.xy.coords)
            texto_surface = self.texto.fonte.render(str(self.id), True, (0, 0, 0))
            texto_rect = texto_surface.get_rect()
            texto_rect.center = texto_screen_pos
            tela.blit(texto_surface, texto_rect)


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
        global camera
        if camera is None:
            return

        # Converte pontos para coordenadas de tela
        inicio_screen = camera.world_to_screen(inicio)
        fim_screen = camera.world_to_screen(fim)

        # Ajusta pontos para não sobrepor aos nós
        dx = fim_screen[0] - inicio_screen[0]
        dy = fim_screen[1] - inicio_screen[1]
        comprimento = math.sqrt(dx * dx + dy * dy)

        if comprimento < 10:
            return

        dx_norm = dx / comprimento
        dy_norm = dy / comprimento

        raio_no = 30 * camera.zoom
        inicio_ajustado = (
            inicio_screen[0] + dx_norm * raio_no,
            inicio_screen[1] + dy_norm * raio_no
        )
        fim_ajustado = (
            fim_screen[0] - dx_norm * raio_no,
            fim_screen[1] - dy_norm * raio_no
        )

        # Calcula os pontos da curva em coordenadas de tela
        pontos_curva = self.calcular_pontos_curva(inicio_ajustado, fim_ajustado, curvatura * camera.zoom)

        # Desenha a curva como uma série de linhas pequenas
        espessura_scaled = max(1, int(espessura * camera.zoom))
        for i in range(len(pontos_curva) - 1):
            pg.draw.line(tela, cor, pontos_curva[i], pontos_curva[i + 1], espessura_scaled)

        # Desenha a ponta da seta no final da curva
        if len(pontos_curva) >= 2:
            ultimo_ponto = pontos_curva[-1]
            penultimo_ponto = pontos_curva[-2]

            # Calcula a direção da seta baseada nos últimos pontos da curva
            dx_seta = ultimo_ponto[0] - penultimo_ponto[0]
            dy_seta = ultimo_ponto[1] - penultimo_ponto[1]
            angulo = math.atan2(dy_seta, dx_seta)

            # Tamanho e ângulo da seta
            tamanho_seta = 25 * camera.zoom
            angulo_seta = math.pi / 6  # 30 graus

            # Pontos da ponta da seta
            x1 = ultimo_ponto[0] - tamanho_seta * math.cos(angulo - angulo_seta)
            y1 = ultimo_ponto[1] - tamanho_seta * math.sin(angulo - angulo_seta)

            x2 = ultimo_ponto[0] - tamanho_seta * math.cos(angulo + angulo_seta)
            y2 = ultimo_ponto[1] - tamanho_seta * math.sin(angulo + angulo_seta)

            # Desenha as linhas da ponta da seta
            pg.draw.line(tela, cor, ultimo_ponto, (x1, y1), espessura_scaled)
            pg.draw.line(tela, cor, ultimo_ponto, (x2, y2), espessura_scaled)

    def desenhar_seta(self, tela, inicio, fim, cor=(255, 255, 255), espessura=10):
        """
        Desenha uma seta reta (método original para compatibilidade)
        """
        global camera
        if camera is None:
            return

        # Converte pontos para coordenadas de tela
        inicio_screen = camera.world_to_screen(inicio)
        fim_screen = camera.world_to_screen(fim)

        # Desenha a linha principal primeiro
        espessura_scaled = max(1, int(espessura * camera.zoom))
        pg.draw.line(tela, cor, inicio_screen, fim_screen, espessura_scaled)

        # Calcula a direção da linha
        dx = fim_screen[0] - inicio_screen[0]
        dy = fim_screen[1] - inicio_screen[1]
        comprimento = math.sqrt(dx * dx + dy * dy)

        if comprimento < 10:  # Linha muito curta
            return

        # Normaliza o vetor direção
        dx_norm = dx / comprimento
        dy_norm = dy / comprimento

        # Ajusta o ponto final para não sobrepor ao nó
        raio_no = 60 * camera.zoom
        fim_ajustado = (
            fim_screen[0] - dx_norm * raio_no,
            fim_screen[1] - dy_norm * raio_no
        )

        # Tamanho e ângulo da seta
        tamanho_seta = 25 * camera.zoom
        angulo = math.atan2(dy, dx)
        angulo_seta = math.pi / 6  # 30 graus

        # Pontos da ponta da seta
        x1 = fim_ajustado[0] - tamanho_seta * math.cos(angulo - angulo_seta)
        y1 = fim_ajustado[1] - tamanho_seta * math.sin(angulo - angulo_seta)

        x2 = fim_ajustado[0] - tamanho_seta * math.cos(angulo + angulo_seta)
        y2 = fim_ajustado[1] - tamanho_seta * math.sin(angulo + angulo_seta)

        # Desenha as linhas da ponta da seta
        pg.draw.line(tela, cor, fim_ajustado, (x1, y1), espessura_scaled)
        pg.draw.line(tela, cor, fim_ajustado, (x2, y2), espessura_scaled)

    def render(self, tela):
        global camera
        if camera is None:
            return

        # Verifica se a linha está visível na tela
        inicio_screen = camera.world_to_screen(self.ponto0.coords)
        fim_screen = camera.world_to_screen(self.ponto1.coords)

        # Renderiza apenas se pelo menos parte da linha estiver visível
        if ((-100 < inicio_screen[0] < camera.width + 100 or -100 < fim_screen[0] < camera.width + 100) and
                (-100 < inicio_screen[1] < camera.height + 100 or -100 < fim_screen[1] < camera.height + 100)):

            if self.direcionada:
                if self.curvatura != 0:
                    # Desenha seta com curva
                    self.desenhar_seta_curva(tela, self.ponto0.coords, self.ponto1.coords, self.curvatura)
                else:
                    # Desenha seta reta
                    self.desenhar_seta(tela, self.ponto0.coords, self.ponto1.coords)
            else:
                # Linha normal sem seta
                espessura_scaled = max(1, int(10 * camera.zoom))
                pg.draw.line(tela, (255, 255, 255), inicio_screen, fim_screen, espessura_scaled)


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