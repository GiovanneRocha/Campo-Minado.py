import pygame
import random
import sys
import time
import json
import os

# Inicializar pygame
pygame.init()

# Configurações do jogo
LARGURA_TELA = 800
ALTURA_TELA = 900
TAMANHO_GRADE = 18
TAMANHO_CELULA = 32
NUM_BOMBAS = 42
MARGEM_X = (LARGURA_TELA - (TAMANHO_GRADE * TAMANHO_CELULA)) // 2
MARGEM_Y = 150

# Cores modernas
CORES = {
    'bg_principal': (45, 52, 62),
    'bg_secundario': (55, 65, 81),
    'bg_topo': (31, 41, 55),
    'celula_coberta': (156, 163, 175),
    'celula_revelada': (243, 244, 246),
    'celula_hover': (209, 213, 219),
    'bomba': (220, 38, 38),
    'bandeira': (239, 68, 68),
    'texto_branco': (255, 255, 255),
    'texto_escuro': (31, 41, 55),
    'sucesso': (34, 197, 94),
    'erro': (239, 68, 68),
    'aviso': (251, 191, 36),
    'botao_hover': (59, 130, 246),
    'sombra': (0, 0, 0, 50),
    'gradiente_1': (59, 130, 246),
    'gradiente_2': (147, 51, 234)
}

# Cores dos números com esquema mais moderno
CORES_NUMEROS = {
    1: (37, 99, 235),    # Azul
    2: (34, 197, 94),    # Verde
    3: (239, 68, 68),    # Vermelho
    4: (147, 51, 234),   # Roxo
    5: (194, 65, 12),    # Laranja escuro
    6: (14, 165, 233),   # Azul claro
    7: (31, 41, 55),     # Quase preto
    8: (107, 114, 128)   # Cinza
}

# Níveis de dificuldade
NIVEIS = {
    'facil': {'grade': 12, 'bombas': 15, 'nome': 'Fácil'},
    'medio': {'grade': 18, 'bombas': 42, 'nome': 'Médio'},
    'dificil': {'grade': 24, 'bombas': 99, 'nome': 'Difícil'}
}

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x, y):
        for _ in range(20):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-5, 5),
                'life': 60,
                'color': random.choice([CORES['bomba'], CORES['aviso'], (255, 255, 255)])
            })
    
    def add_victory(self, x, y):
        for _ in range(15):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-8, -2),
                'life': 120,
                'color': random.choice([CORES['sucesso'], CORES['aviso'], (255, 255, 255)])
            })
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravidade
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        for particle in self.particles:
            alpha = max(0, particle['life'] / 60 * 255)
            color = (*particle['color'], int(alpha))
            size = max(1, particle['life'] // 20)
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), size)

class CampoMinado:
    def __init__(self):
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Campo Minado - Versão Aprimorada")
        self.clock = pygame.time.Clock()
        
        # Fontes
        self.fonte_pequena = pygame.font.Font(None, 20)
        self.fonte_media = pygame.font.Font(None, 28)
        self.fonte_grande = pygame.font.Font(None, 36)
        self.fonte_titulo = pygame.font.Font(None, 48)
        
        # Sistema de partículas
        self.particles = ParticleSystem()
        
        # Estado do jogo
        self.nivel_atual = 'medio'
        self.mouse_pos = (0, 0)
        self.celula_hover = None
        self.tempo_inicio = 0
        self.tempo_final = 0
        self.recordes = self.carregar_recordes()
        self.animacao_vitoria = 0
        self.primeira_vitoria = True
        
        # Configurar nível
        self.configurar_nivel()
        self.reiniciar_jogo()
    
    def configurar_nivel(self):
        config = NIVEIS[self.nivel_atual]
        global TAMANHO_GRADE, NUM_BOMBAS, MARGEM_X, MARGEM_Y
        TAMANHO_GRADE = config['grade']
        NUM_BOMBAS = config['bombas']
        MARGEM_X = (LARGURA_TELA - (TAMANHO_GRADE * TAMANHO_CELULA)) // 2
        MARGEM_Y = 150
    
    def carregar_recordes(self):
        try:
            if os.path.exists('recordes.json'):
                with open('recordes.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'facil': None, 'medio': None, 'dificil': None}
    
    def salvar_recordes(self):
        try:
            with open('recordes.json', 'w') as f:
                json.dump(self.recordes, f)
        except:
            pass
    
    def reiniciar_jogo(self):
        self.tabuleiro = [[0 for _ in range(TAMANHO_GRADE)] for _ in range(TAMANHO_GRADE)]
        self.revelado = [[False for _ in range(TAMANHO_GRADE)] for _ in range(TAMANHO_GRADE)]
        self.marcado = [[False for _ in range(TAMANHO_GRADE)] for _ in range(TAMANHO_GRADE)]
        self.jogo_terminado = False
        self.vitoria = False
        self.primeiro_clique = True
        self.bombas_restantes = NUM_BOMBAS
        self.tempo_inicio = time.time()
        self.tempo_final = 0
        self.animacao_vitoria = 0
        self.particles.particles.clear()
    
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
            self.tempo_final = time.time()
            # Efeito de explosão
            x = MARGEM_X + coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2
            y = MARGEM_Y + linha * TAMANHO_CELULA + TAMANHO_CELULA // 2
            self.particles.add_explosion(x, y)
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
        
        if not self.vitoria:
            self.vitoria = True
            self.jogo_terminado = True
            self.tempo_final = time.time()
            
            # Verificar recorde
            tempo_jogo = int(self.tempo_final - self.tempo_inicio)
            if (self.recordes[self.nivel_atual] is None or 
                tempo_jogo < self.recordes[self.nivel_atual]):
                self.recordes[self.nivel_atual] = tempo_jogo
                self.salvar_recordes()
                self.primeira_vitoria = False
            
            # Efeito de vitória
            for _ in range(5):
                x = random.randint(MARGEM_X, MARGEM_X + TAMANHO_GRADE * TAMANHO_CELULA)
                y = random.randint(MARGEM_Y, MARGEM_Y + TAMANHO_GRADE * TAMANHO_CELULA)
                self.particles.add_victory(x, y)
        
        return True
    
    def obter_posicao_mouse(self, pos_mouse):
        x, y = pos_mouse
        if (MARGEM_X <= x < MARGEM_X + TAMANHO_GRADE * TAMANHO_CELULA and
            MARGEM_Y <= y < MARGEM_Y + TAMANHO_GRADE * TAMANHO_CELULA):
            coluna = (x - MARGEM_X) // TAMANHO_CELULA
            linha = (y - MARGEM_Y) // TAMANHO_CELULA
            return linha, coluna
        return None, None
    
    def desenhar_gradiente(self, surface, color1, color2, rect):
        """Desenha um gradiente vertical"""
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), 
                           (rect.x, rect.y + y), 
                           (rect.x + rect.width, rect.y + y))
    
    def desenhar_botao(self, texto, x, y, width, height, cor_fundo, cor_texto, hover=False):
        """Desenha um botão estilizado"""
        rect = pygame.Rect(x, y, width, height)
        
        # Sombra
        sombra_rect = pygame.Rect(x + 2, y + 2, width, height)
        pygame.draw.rect(self.tela, (0, 0, 0, 100), sombra_rect, border_radius=8)
        
        # Botão principal
        if hover:
            pygame.draw.rect(self.tela, CORES['botao_hover'], rect, border_radius=8)
        else:
            pygame.draw.rect(self.tela, cor_fundo, rect, border_radius=8)
        
        # Borda
        pygame.draw.rect(self.tela, CORES['bg_secundario'], rect, 2, border_radius=8)
        
        # Texto
        texto_surface = self.fonte_media.render(texto, True, cor_texto)
        texto_rect = texto_surface.get_rect(center=rect.center)
        self.tela.blit(texto_surface, texto_rect)
        
        return rect
    
    def desenhar_tabuleiro(self):
        for linha in range(TAMANHO_GRADE):
            for coluna in range(TAMANHO_GRADE):
                x = MARGEM_X + coluna * TAMANHO_CELULA
                y = MARGEM_Y + linha * TAMANHO_CELULA
                rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
                
                # Efeito hover
                is_hover = (self.celula_hover == (linha, coluna) and 
                           not self.revelado[linha][coluna] and 
                           not self.jogo_terminado)
                
                # Desenhar célula
                if self.revelado[linha][coluna]:
                    pygame.draw.rect(self.tela, CORES['celula_revelada'], rect, border_radius=4)
                    
                    if self.tabuleiro[linha][coluna] == -1:
                        # Desenhar bomba com efeito
                        centro = (x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2)
                        pygame.draw.circle(self.tela, CORES['bomba'], centro, TAMANHO_CELULA // 3)
                        pygame.draw.circle(self.tela, (255, 255, 255), centro, TAMANHO_CELULA // 6)
                    elif self.tabuleiro[linha][coluna] > 0:
                        # Desenhar número
                        cor = CORES_NUMEROS.get(self.tabuleiro[linha][coluna], CORES['texto_escuro'])
                        texto = self.fonte_grande.render(str(self.tabuleiro[linha][coluna]), True, cor)
                        texto_rect = texto.get_rect(center=rect.center)
                        self.tela.blit(texto, texto_rect)
                else:
                    # Célula coberta
                    cor_celula = CORES['celula_hover'] if is_hover else CORES['celula_coberta']
                    pygame.draw.rect(self.tela, cor_celula, rect, border_radius=4)
                    
                    if self.marcado[linha][coluna]:
                        # Desenhar bandeira moderna
                        centro_x = x + TAMANHO_CELULA // 2
                        centro_y = y + TAMANHO_CELULA // 2
                        
                        # Haste
                        pygame.draw.line(self.tela, CORES['texto_escuro'], 
                                       (centro_x - 2, centro_y - 8), 
                                       (centro_x - 2, centro_y + 8), 3)
                        
                        # Bandeira
                        pontos = [
                            (centro_x, centro_y - 8),
                            (centro_x + 10, centro_y - 3),
                            (centro_x, centro_y + 2)
                        ]
                        pygame.draw.polygon(self.tela, CORES['bandeira'], pontos)
                
                # Borda sutil
                pygame.draw.rect(self.tela, CORES['bg_secundario'], rect, 1, border_radius=4)
    
    def desenhar_interface(self):
        # Fundo com gradiente
        self.desenhar_gradiente(self.tela, CORES['bg_principal'], CORES['bg_secundario'], 
                              pygame.Rect(0, 0, LARGURA_TELA, ALTURA_TELA))
        
        # Barra superior
        barra_rect = pygame.Rect(0, 0, LARGURA_TELA, 120)
        pygame.draw.rect(self.tela, CORES['bg_topo'], barra_rect)
        
        # Título
        titulo = self.fonte_titulo.render("Campo Minado", True, CORES['texto_branco'])
        self.tela.blit(titulo, (20, 20))
        
        # Informações do jogo
        tempo_atual = int(time.time() - self.tempo_inicio) if not self.jogo_terminado else int(self.tempo_final - self.tempo_inicio)
        info_y = 70
        
        # Bombas restantes
        texto_bombas = self.fonte_media.render(f"💣 {self.bombas_restantes}", True, CORES['texto_branco'])
        self.tela.blit(texto_bombas, (20, info_y))
        
        # Tempo
        texto_tempo = self.fonte_media.render(f"⏱️ {tempo_atual}s", True, CORES['texto_branco'])
        self.tela.blit(texto_tempo, (150, info_y))
        
        # Nível atual
        nome_nivel = NIVEIS[self.nivel_atual]['nome']
        texto_nivel = self.fonte_media.render(f"🎯 {nome_nivel}", True, CORES['texto_branco'])
        self.tela.blit(texto_nivel, (280, info_y))
        
        # Recorde
        if self.recordes[self.nivel_atual]:
            texto_recorde = self.fonte_media.render(f"🏆 {self.recordes[self.nivel_atual]}s", True, CORES['aviso'])
            self.tela.blit(texto_recorde, (410, info_y))
        
        # Botões
        botoes = {}
        
        # Botão reiniciar
        botoes['reiniciar'] = self.desenhar_botao("🔄 Reiniciar", LARGURA_TELA - 120, 20, 100, 35, 
                                                  CORES['sucesso'], CORES['texto_branco'])
        
        # Botões de nível
        x_nivel = LARGURA_TELA - 320
        for i, (nivel, config) in enumerate(NIVEIS.items()):
            cor = CORES['botao_hover'] if nivel == self.nivel_atual else CORES['bg_secundario']
            botoes[nivel] = self.desenhar_botao(config['nome'], x_nivel + i * 70, 60, 65, 30, 
                                               cor, CORES['texto_branco'])
        
        # Mensagem de status
        if self.jogo_terminado:
            if self.vitoria:
                self.animacao_vitoria += 1
                pulse = 1 + 0.1 * abs(pygame.math.Vector2(1, 0).rotate(self.animacao_vitoria * 5).x)
                
                if not self.primeira_vitoria and self.recordes[self.nivel_atual] == int(self.tempo_final - self.tempo_inicio):
                    mensagem = "🎉 NOVO RECORDE! 🎉"
                    cor = CORES['aviso']
                else:
                    mensagem = "🎉 VITÓRIA! 🎉"
                    cor = CORES['sucesso']
            else:
                mensagem = "💥 GAME OVER!"
                cor = CORES['erro']
                pulse = 1
            
            # Fundo da mensagem
            msg_surface = self.fonte_titulo.render(mensagem, True, cor)
            msg_rect = msg_surface.get_rect(center=(LARGURA_TELA // 2, MARGEM_Y - 30))
            
            # Escalar para efeito pulse
            if pulse != 1:
                msg_surface = pygame.transform.scale(msg_surface, 
                                                   (int(msg_rect.width * pulse), 
                                                    int(msg_rect.height * pulse)))
                msg_rect = msg_surface.get_rect(center=(LARGURA_TELA // 2, MARGEM_Y - 30))
            
            # Sombra
            sombra_rect = msg_rect.copy()
            sombra_rect.x += 2
            sombra_rect.y += 2
            pygame.draw.rect(self.tela, (0, 0, 0, 100), sombra_rect, border_radius=10)
            
            # Fundo
            pygame.draw.rect(self.tela, CORES['bg_topo'], msg_rect.inflate(20, 10), border_radius=10)
            self.tela.blit(msg_surface, msg_rect)
        
        # Desenhar tabuleiro
        self.desenhar_tabuleiro()
        
        # Desenhar partículas
        self.particles.update()
        self.particles.draw(self.tela)
        
        return botoes
    
    def executar(self):
        rodando = True
        
        while rodando:
            self.mouse_pos = pygame.mouse.get_pos()
            self.celula_hover = self.obter_posicao_mouse(self.mouse_pos)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = pygame.mouse.get_pos()
                    botoes = self.desenhar_interface()
                    
                    # Verificar clique nos botões
                    clicou_botao = False
                    for nome, rect in botoes.items():
                        if rect.collidepoint(pos_mouse):
                            clicou_botao = True
                            if nome == 'reiniciar':
                                self.reiniciar_jogo()
                            elif nome in NIVEIS:
                                self.nivel_atual = nome
                                self.configurar_nivel()
                                self.reiniciar_jogo()
                            break
                    
                    if not clicou_botao:
                        # Verificar clique no tabuleiro
                        linha, coluna = self.obter_posicao_mouse(pos_mouse)
                        if linha is not None and coluna is not None and not self.jogo_terminado:
                            if evento.button == 1:  # Clique esquerdo
                                self.revelar_celula(linha, coluna)
                            elif evento.button == 3:  # Clique direito
                                self.marcar_celula(linha, coluna)
                
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        self.reiniciar_jogo()
                    elif evento.key == pygame.K_1:
                        self.nivel_atual = 'facil'
                        self.configurar_nivel()
                        self.reiniciar_jogo()
                    elif evento.key == pygame.K_2:
                        self.nivel_atual = 'medio'
                        self.configurar_nivel()
                        self.reiniciar_jogo()
                    elif evento.key == pygame.K_3:
                        self.nivel_atual = 'dificil'
                        self.configurar_nivel()
                        self.reiniciar_jogo()
            
            if not self.jogo_terminado:
                self.verificar_vitoria()
            
            # Desenhar tudo
            self.desenhar_interface()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Executar o jogo
if __name__ == "__main__":
    jogo = CampoMinado()
    jogo.executar()
