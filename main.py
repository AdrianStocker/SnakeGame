import pygame
import random
import sys

pygame.init()

# Configurações da tela
LARGURA, ALTURA = 600, 600
HUD_ALTURA = 80  # área extra para scores
TAMANHO_QUADRADO = 10 #Tamanho dos quadrados que formam a cobra e a maçã

tela = pygame.display.set_mode((LARGURA, ALTURA + HUD_ALTURA))
pygame.display.set_caption("Snake Game")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
AZUL = (0, 150, 200)
VERMELHO = (255, 0, 0)
DOURADO = (255, 215, 0)
CINZA = (40, 40, 40)

# Cabeças mais escuras
VERDE_ESCURO = (0, 150, 0)
AZUL_ESCURO = (0, 100, 150)

# Fonte
fonte = pygame.font.SysFont("Arial", 30, bold=True)
fonte_grande = pygame.font.SysFont("Arial", 50, bold=True)

clock = pygame.time.Clock()
highscore = 0  # recorde global para singleplayer

# ---------------- Funções ---------------- #

def desenhar_grade():
    for x in range(0, LARGURA, TAMANHO_QUADRADO):
        pygame.draw.line(tela, CINZA, (x, HUD_ALTURA), (x, ALTURA + HUD_ALTURA))
    for y in range(HUD_ALTURA, ALTURA + HUD_ALTURA, TAMANHO_QUADRADO):
        pygame.draw.line(tela, CINZA, (0, y), (LARGURA, y))

def desenhar_borda():
    pygame.draw.rect(tela, BRANCO, (0, HUD_ALTURA, LARGURA, ALTURA), 3)

def mostrar_score_single(score):
    global highscore
    texto_score = fonte.render(f"Score: {score}", True, BRANCO)
    tela.blit(texto_score, (10, 20))
    highscore = max(highscore, score)
    texto_high = fonte.render(f"Recorde: {highscore}", True, DOURADO)
    tela.blit(texto_high, (200, 20))

def mostrar_score_multi(score1, score2):
    texto_p1 = fonte.render(f"P1: {score1}", True, VERDE)
    tela.blit(texto_p1, (10, 20))
    texto_p2 = fonte.render(f"P2: {score2}", True, AZUL)
    tela.blit(texto_p2, (200, 20))

def tela_game_over(modo, vencedor=None):
    rodando = True
    while rodando:
        tela.fill(PRETO)

        # Texto principal
        if modo == "single":
            texto = fonte_grande.render("GAME OVER", True, VERMELHO)
            rect = texto.get_rect(center=(LARGURA // 2, (ALTURA + HUD_ALTURA)//2 - 100))
            tela.blit(texto, rect)
            recorde_texto = fonte.render(f"Recorde: {highscore}", True, DOURADO)
            rect = recorde_texto.get_rect(center=(LARGURA // 2, (ALTURA + HUD_ALTURA)//2 - 50))
            tela.blit(recorde_texto, rect)
        else:
            texto = fonte_grande.render("GAME OVER", True, VERMELHO)
            rect = texto.get_rect(center=(LARGURA // 2, (ALTURA + HUD_ALTURA)//2 - 100))
            tela.blit(texto, rect)
            if vencedor:
                vencedor_texto = fonte.render(f"Vencedor: {vencedor}", True, VERDE)
                rect = vencedor_texto.get_rect(center=(LARGURA // 2, (ALTURA + HUD_ALTURA)//2 - 50))
                tela.blit(vencedor_texto, rect)

        # Botões
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        jogar_novamente = pygame.Rect(LARGURA//2 - 120, (ALTURA + HUD_ALTURA)//2 + 20, 240, 50)
        sair_jogo = pygame.Rect(LARGURA//2 - 120, (ALTURA + HUD_ALTURA)//2 + 160, 240, 50)
        menu_inicial = pygame.Rect(LARGURA//2 - 120, (ALTURA + HUD_ALTURA)//2 + 90, 240, 50)

        pygame.draw.rect(tela, AZUL if jogar_novamente.collidepoint(mouse) else CINZA, jogar_novamente)
        pygame.draw.rect(tela, AZUL if sair_jogo.collidepoint(mouse) else CINZA, sair_jogo)
        pygame.draw.rect(tela, AZUL if menu_inicial.collidepoint(mouse) else CINZA, menu_inicial)

        jogar_texto = fonte.render("Jogar Novamente", True, BRANCO)
        sair_texto = fonte.render("Sair", True, BRANCO)
        menu_texto = fonte.render("Menu Inicial", True, BRANCO)

        tela.blit(jogar_texto, jogar_texto.get_rect(center=jogar_novamente.center))
        tela.blit(sair_texto, sair_texto.get_rect(center=sair_jogo.center))
        tela.blit(menu_texto, menu_texto.get_rect(center=menu_inicial.center))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if jogar_novamente.collidepoint(mouse) and clique[0]:
            return "reiniciar"
        if sair_jogo.collidepoint(mouse) and clique[0]:
            pygame.quit()
            sys.exit()
        if menu_inicial.collidepoint(mouse) and clique[0]:
            return "menu"

        pygame.display.flip()

# ---------------- Função principal do jogo ---------------- #
def jogo(modo):
    global highscore
    cobra1 = [[100, HUD_ALTURA + 100]]
    cobra2 = [[400, HUD_ALTURA + 100]]
    direcao1 = "DIREITA"
    direcao2 = "ESQUERDA"

    maca = [random.randrange(0, LARGURA, TAMANHO_QUADRADO),
            random.randrange(HUD_ALTURA, ALTURA + HUD_ALTURA, TAMANHO_QUADRADO)]

    score1 = 0
    score2 = 0
    velocidade1 = 10
    velocidade2 = 10

    rodando = True
    while rodando:
        tela.fill(PRETO)
        desenhar_grade()
        desenhar_borda()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                # Player 1
                if evento.key == pygame.K_UP and direcao1 != "BAIXO": direcao1 = "CIMA"
                if evento.key == pygame.K_DOWN and direcao1 != "CIMA": direcao1 = "BAIXO"
                if evento.key == pygame.K_LEFT and direcao1 != "DIREITA": direcao1 = "ESQUERDA"
                if evento.key == pygame.K_RIGHT and direcao1 != "ESQUERDA": direcao1 = "DIREITA"
                # Player 2
                if modo == "multi":
                    if evento.key == pygame.K_w and direcao2 != "BAIXO": direcao2 = "CIMA"
                    if evento.key == pygame.K_s and direcao2 != "CIMA": direcao2 = "BAIXO"
                    if evento.key == pygame.K_a and direcao2 != "DIREITA": direcao2 = "ESQUERDA"
                    if evento.key == pygame.K_d and direcao2 != "ESQUERDA": direcao2 = "DIREITA"

        # mover cobras
        # cobra1
        if direcao1 == "CIMA": nova_cabeca1 = [cobra1[0][0], cobra1[0][1] - TAMANHO_QUADRADO]
        elif direcao1 == "BAIXO": nova_cabeca1 = [cobra1[0][0], cobra1[0][1] + TAMANHO_QUADRADO]
        elif direcao1 == "ESQUERDA": nova_cabeca1 = [cobra1[0][0] - TAMANHO_QUADRADO, cobra1[0][1]]
        else: nova_cabeca1 = [cobra1[0][0] + TAMANHO_QUADRADO, cobra1[0][1]]
        cobra1.insert(0, nova_cabeca1)

        # cobra2
        if modo == "multi":
            if direcao2 == "CIMA": nova_cabeca2 = [cobra2[0][0], cobra2[0][1] - TAMANHO_QUADRADO]
            elif direcao2 == "BAIXO": nova_cabeca2 = [cobra2[0][0], cobra2[0][1] + TAMANHO_QUADRADO]
            elif direcao2 == "ESQUERDA": nova_cabeca2 = [cobra2[0][0] - TAMANHO_QUADRADO, cobra2[0][1]]
            else: nova_cabeca2 = [cobra2[0][0] + TAMANHO_QUADRADO, cobra2[0][1]]
            cobra2.insert(0, nova_cabeca2)

        # comer maçã
        if cobra1[0] == maca:
            score1 += 1
            maca = [random.randrange(0, LARGURA, TAMANHO_QUADRADO),
                    random.randrange(HUD_ALTURA, ALTURA + HUD_ALTURA, TAMANHO_QUADRADO)]
        else: cobra1.pop()

        if modo == "multi":
            if cobra2[0] == maca:
                score2 += 1
                maca = [random.randrange(0, LARGURA, TAMANHO_QUADRADO),
                        random.randrange(HUD_ALTURA, ALTURA + HUD_ALTURA, TAMANHO_QUADRADO)]
            else: cobra2.pop()

        # colisões
        morreu = False
        vencedor = None

        if (cobra1[0][0] < 0 or cobra1[0][0] >= LARGURA or
            cobra1[0][1] < HUD_ALTURA or cobra1[0][1] >= ALTURA + HUD_ALTURA or
            cobra1[0] in cobra1[1:]):
            morreu = True
            vencedor = "Player 2" if modo == "multi" else None

        if modo == "multi":
            if (cobra2[0][0] < 0 or cobra2[0][0] >= LARGURA or
                cobra2[0][1] < HUD_ALTURA or cobra2[0][1] >= ALTURA + HUD_ALTURA or
                cobra2[0] in cobra2[1:]):
                morreu = True
                vencedor = "Player 1"

            # colisão entre cobras
            if cobra1[0] in cobra2:
                morreu = True
                vencedor = "Player 2"
            if cobra2[0] in cobra1:
                morreu = True
                vencedor = "Player 1"

        if morreu:
            acao = tela_game_over(modo, vencedor)
            if acao == "reiniciar":
                return jogo(modo)
            elif acao == "menu":
                return menu()
            else:
                pygame.quit()
                sys.exit()

        # desenhar maçã
        pygame.draw.rect(tela, VERMELHO, (maca[0], maca[1], TAMANHO_QUADRADO, TAMANHO_QUADRADO))

        # desenhar cobras com cabeça mais escura
        for i, parte in enumerate(cobra1):
            cor = VERDE_ESCURO if i == 0 else VERDE
            pygame.draw.rect(tela, cor, (parte[0], parte[1], TAMANHO_QUADRADO, TAMANHO_QUADRADO))
        if modo == "multi":
            for i, parte in enumerate(cobra2):
                cor = AZUL_ESCURO if i == 0 else AZUL
                pygame.draw.rect(tela, cor, (parte[0], parte[1], TAMANHO_QUADRADO, TAMANHO_QUADRADO))

        # mostrar scores
        if modo == "single":
            mostrar_score_single(score1)
        else:
            mostrar_score_multi(score1, score2)

        pygame.display.flip()

        # aumentar velocidade a cada múltiplo de 5
        velocidade1 = 10 + (score1 // 5) * 2
        if modo == "multi": velocidade2 = 10 + (score2 // 5) * 2

        clock.tick(max(velocidade1, velocidade2))

# ---------------- Menu Inicial ---------------- #
def menu():
    modo = None
    while modo is None:
        tela.fill(PRETO)
        titulo = fonte_grande.render("Snake Game", True, BRANCO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 150))

        btn_single = fonte.render("1 - Singleplayer", True, VERDE)
        tela.blit(btn_single, (LARGURA//2 - btn_single.get_width()//2, 250))
        btn_multi = fonte.render("2 - Multiplayer", True, AZUL)
        tela.blit(btn_multi, (LARGURA//2 - btn_multi.get_width()//2, 300))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    modo = "single"
                elif evento.key == pygame.K_2:
                    modo = "multi"
    jogo(modo)

menu()
