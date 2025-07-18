import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Configurações do jogo
LARGURA_TELA = 600
ALTURA_TELA = 700
TAMANHO_GRADE = 18
TAMANHO_CELULA = 32
NUM_BOMBAS = 42
MARGEM_X = (LARGURA_TELA - (TAMANHO_GRADE * TAMANHO_CELULA)) // 2
MARGEM_Y = 100

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (192, 192, 192)
CINZA_ESCURO = (128, 128, 128)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)
MARROM = (165, 42, 42)
ROSA = (255, 192, 203)

# Cores dos números
CORES_NUMEROS = {
    1: AZUL,
    2: VERDE,
    3: VERMELHO,
    4: ROXO,
    5: MARROM,
    6: (0, 128, 128),
    7: PRETO,
    8: CINZA_ESCURO
}

class CampoMinado:
    def __init__(self):
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Campo Minado")
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 24)
        self.fonte_grande = pygame.font.Font(None, 36)
        
        self.reiniciar_jogo()
    
    def reiniciar_jogo(self):
        self.tabuleiro = [[0 for _ in range(TAMANHO_GRADE)] for _ in range(TAMANHO_GRADE)]
        self.revelado = [[False for _ in range(TAMANHO_GRADE)] for _ in range(TAMANHO_GRADE)]
        self.marcado = [[False for _ in range(TAMANHO_GRADE)] for _ in range(TAMANHO_GRADE)]
        self.jogo_terminado = False
        self.vitoria = False
        self.primeiro_clique = True
        self.bombas_restantes = NUM_BOMBAS
        
    def colocar_bombas(self, primeira_linha, primeira_coluna):
        bombas_colocadas = 0
        while bombas_colocadas < NUM_BOMBAS:
            linha = random.randint(0, TAMANHO_GRADE - 1)
            coluna = random.randint(0, TAMANHO_GRADE - 1)
            
            # Não colocar bomba na primeira célula clicada ou nas adjacentes
            if (abs(linha - primeira_linha) <= 1 and abs(coluna - primeira_coluna) <= 1):
                continue
                
            if self.tabuleiro[linha][coluna] != -1:
                self.tabuleiro[linha][coluna] = -1
                bombas_colocadas += 1
                
                # Incrementar números nas células adjacentes
                for dl in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nl, nc = linha + dl, coluna + dc
                        if (0 <= nl < TAMANHO_GRADE and 0 <= nc < TAMANHO_GRADE and 
                            self.tabuleiro[nl][nc] != -1):
                            self.tabuleiro[nl][nc] += 1
    
    def revelar_celula(self, linha, coluna):
        if (linha < 0 or linha >= TAMANHO_GRADE or coluna < 0 or coluna >= TAMANHO_GRADE or
            self.revelado[linha][coluna] or self.marcado[linha][coluna]):
            return
        
        if self.primeiro_clique:
            self.colocar_bombas(linha, coluna)
            self.primeiro_clique = False
        
        self.revelado[linha][coluna] = True
        
        if self.tabuleiro[linha][coluna] == -1:
            self.jogo_terminado = True
            return
        
        # Se a célula está vazia, revelar células adjacentes
        if self.tabuleiro[linha][coluna] == 0:
            for dl in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    self.revelar_celula(linha + dl, coluna + dc)
    
    def marcar_celula(self, linha, coluna):
        if not self.revelado[linha][coluna]:
            self.marcado[linha][coluna] = not self.marcado[linha][coluna]
            if self.marcado[linha][coluna]:
                self.bombas_restantes -= 1
            else:
                self.bombas_restantes += 1
    
    def verificar_vitoria(self):
        for linha in range(TAMANHO_GRADE):
            for coluna in range(TAMANHO_GRADE):
                if (self.tabuleiro[linha][coluna] != -1 and not self.revelado[linha][coluna]):
                    return False
        self.vitoria = True
        self.jogo_terminado = True
        return True
    
    def obter_posicao_mouse(self, pos_mouse):
        x, y = pos_mouse
        if (MARGEM_X <= x < MARGEM_X + TAMANHO_GRADE * TAMANHO_CELULA and
            MARGEM_Y <= y < MARGEM_Y + TAMANHO_GRADE * TAMANHO_CELULA):
            coluna = (x - MARGEM_X) // TAMANHO_CELULA
            linha = (y - MARGEM_Y) // TAMANHO_CELULA
            return linha, coluna
        return None, None
    
    def desenhar_tabuleiro(self):
        for linha in range(TAMANHO_GRADE):
            for coluna in range(TAMANHO_GRADE):
                x = MARGEM_X + coluna * TAMANHO_CELULA
                y = MARGEM_Y + linha * TAMANHO_CELULA
                
                # Desenhar célula
                if self.revelado[linha][coluna]:
                    pygame.draw.rect(self.tela, BRANCO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
                    
                    if self.tabuleiro[linha][coluna] == -1:
                        # Desenhar bomba
                        pygame.draw.circle(self.tela, PRETO, 
                                         (x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2), 
                                         TAMANHO_CELULA // 3)
                    elif self.tabuleiro[linha][coluna] > 0:
                        # Desenhar número
                        cor = CORES_NUMEROS.get(self.tabuleiro[linha][coluna], PRETO)
                        texto = self.fonte.render(str(self.tabuleiro[linha][coluna]), True, cor)
                        texto_rect = texto.get_rect(center=(x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2))
                        self.tela.blit(texto, texto_rect)
                else:
                    pygame.draw.rect(self.tela, CINZA, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
                    
                    if self.marcado[linha][coluna]:
                        # Desenhar bandeira
                        pygame.draw.polygon(self.tela, VERMELHO, [
                            (x + 5, y + 5),
                            (x + 20, y + 10),
                            (x + 5, y + 15)
                        ])
                        pygame.draw.line(self.tela, PRETO, (x + 5, y + 5), (x + 5, y + 25), 2)
                
                # Desenhar bordas
                pygame.draw.rect(self.tela, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)
    
    def desenhar_interface(self):
        self.tela.fill(CINZA_ESCURO)
        
        # Desenhar informações do jogo
        texto_bombas = self.fonte_grande.render(f"Bombas: {self.bombas_restantes}", True, BRANCO)
        self.tela.blit(texto_bombas, (10, 10))
        
        # Botão reiniciar
        botao_rect = pygame.Rect(LARGURA_TELA - 120, 10, 100, 40)
        pygame.draw.rect(self.tela, VERDE, botao_rect)
        texto_botao = self.fonte.render("Reiniciar", True, PRETO)
        texto_rect = texto_botao.get_rect(center=botao_rect.center)
        self.tela.blit(texto_botao, texto_rect)
        
        # Mensagem de status
        if self.jogo_terminado:
            if self.vitoria:
                mensagem = "VITÓRIA! Parabéns!"
                cor = VERDE
            else:
                mensagem = "GAME OVER! Tente novamente."
                cor = VERMELHO
            
            texto_status = self.fonte_grande.render(mensagem, True, cor)
            texto_rect = texto_status.get_rect(center=(LARGURA_TELA // 2, 60))
            self.tela.blit(texto_status, texto_rect)
        
        # Desenhar tabuleiro
        self.desenhar_tabuleiro()
        
        return botao_rect
    
    def executar(self):
        rodando = True
        
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = pygame.mouse.get_pos()
                    
                    # Verificar clique no botão reiniciar
                    botao_rect = pygame.Rect(LARGURA_TELA - 120, 10, 100, 40)
                    if botao_rect.collidepoint(pos_mouse):
                        self.reiniciar_jogo()
                        continue
                    
                    # Verificar clique no tabuleiro
                    linha, coluna = self.obter_posicao_mouse(pos_mouse)
                    if linha is not None and coluna is not None and not self.jogo_terminado:
                        if evento.button == 1:  # Clique esquerdo
                            self.revelar_celula(linha, coluna)
                        elif evento.button == 3:  # Clique direito
                            self.marcar_celula(linha, coluna)
            
            if not self.jogo_terminado:
                self.verificar_vitoria()
            
            # Desenhar tudo
            botao_rect = self.desenhar_interface()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Executar o jogo
if __name__ == "__main__":
    jogo = CampoMinado()
    jogo.executar()