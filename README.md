# Campo Minado 💣

Um jogo clássico de Campo Minado implementado em Python com Pygame, oferecendo uma experiência visual moderna e desafiadora com interface gráfica intuitiva.

## 📋 Descrição

O Campo Minado é um jogo de lógica onde o objetivo é limpar um campo minado sem detonar nenhuma mina. O jogador deve usar pistas numéricas para determinar onde as minas estão localizadas e marcar as células suspeitas com bandeiras. Este projeto implementa uma versão moderna do clássico jogo com gráficos coloridos e controles responsivos.

### ✨ Funcionalidades

- **Interface Gráfica Moderna**: Desenvolvida com Pygame para uma experiência visual aprimorada
- **Campo 18x18**: Tabuleiro de tamanho intermediário com 42 bombas
- **Sistema de Marcação**: Marque células suspeitas com bandeiras vermelhas
- **Contador de Bombas**: Acompanhe quantas bombas restam para marcar
- **Proteção no Primeiro Clique**: Garante que o primeiro clique nunca seja uma bomba
- **Revelação Automática**: Células vazias revelam automaticamente áreas adjacentes
- **Cores Diferenciadas**: Cada número tem sua própria cor para melhor visualização
- **Botão Reiniciar**: Comece uma nova partida instantaneamente
- **Detecção de Vitória**: Sistema automático de verificação de vitória

## 🎮 Como Jogar

### Controles
- **Clique Esquerdo**: Revela uma célula
- **Clique Direito**: Marca/desmarca uma célula com bandeira vermelha
- **Botão Reiniciar**: Inicia uma nova partida

### Objetivo
1. **Revelar todas as células** que não contêm bombas
2. **Usar os números** como pistas - eles indicam quantas bombas estão nas 8 células adjacentes
3. **Marcar células suspeitas** com bandeiras para não clicar nelas acidentalmente
4. **Evitar as bombas**: Se clicar em uma bomba, o jogo termina

### 🎯 Especificações do Jogo

- **Tamanho do Campo**: 18x18 células (324 células total)
- **Número de Bombas**: 42 bombas
- **Dificuldade**: Intermediária (13% das células contêm bombas)
- **Primeira Jogada Segura**: O primeiro clique nunca será uma bomba

### 🎨 Sistema de Cores

Os números são exibidos em cores diferentes para facilitar a identificação:
- **1**: Azul
- **2**: Verde  
- **3**: Vermelho
- **4**: Roxo
- **5**: Marrom
- **6**: Azul petróleo
- **7**: Preto
- **8**: Cinza escuro

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.6 ou superior
- Pygame (biblioteca para jogos em Python)

### Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/GiovanneRocha/Campo-Minado.py.git
cd Campo-Minado.py
```

2. **Instale o Pygame**:
```bash
pip install pygame
```

Ou se você estiver usando Python 3:
```bash
pip3 install pygame
```

3. **Execute o jogo**:
```bash
python campo_minado.py
```

Ou:
```bash
python3 campo_minado.py
```

### Instalação Alternativa (usando requirements.txt)

Se você preferir usar um arquivo de dependências:

1. Crie um arquivo `requirements.txt`:
```
pygame>=2.0.0
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎲 Instruções Detalhadas

### Iniciando o Jogo
- O jogo abre com um campo 18x18 totalmente coberto
- Contador de bombas mostra "42" no canto superior esquerdo
- Botão "Reiniciar" disponível no canto superior direito

### Durante o Jogo
- **Células Cobertas**: Aparecem em cinza
- **Células Reveladas**: Aparecem em branco
- **Números**: Mostram quantas bombas estão nas células adjacentes
- **Bandeiras**: Triângulos vermelhos indicam células marcadas
- **Bombas**: Círculos pretos (visíveis apenas quando o jogo termina)

### Fim do Jogo
- **Vitória**: Quando todas as células sem bomba são reveladas
- **Derrota**: Quando uma bomba é clicada
- **Reiniciar**: Clique no botão verde para jogar novamente

## 🏆 Estratégias e Dicas

### Estratégias Básicas
- **Comece pelas bordas**: Células nas bordas têm menos vizinhos
- **Use a lógica**: Se uma célula "1" já tem uma bandeira adjacente, as outras células ao redor são seguras
- **Procure padrões**: Números isolados frequentemente indicam bombas óbvias

### Padrões Comuns
- **Células "1" em cantos**: Geralmente têm a bomba na diagonal
- **Sequência "1-2-1"**: A bomba geralmente está no meio
- **Células "8"**: Todas as células adjacentes são bombas

### Dicas Avançadas
- Conte as bandeiras ao redor de números revelados
- Use o processo de eliminação
- Quando em dúvida, escolha células mais afastadas de números altos

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem principal
- **Pygame**: Biblioteca para interface gráfica e jogos
- **Random**: Geração aleatória de posições das bombas
- **Sys**: Controle do sistema (fechar o jogo)

## ⚙️ Configurações Técnicas

### Constantes do Jogo
- **Resolução da Tela**: 600x700 pixels
- **Tamanho das Células**: 32x32 pixels
- **Taxa de Quadros**: 60 FPS
- **Fonte**: Padrão do sistema (24px para números, 36px para interface)

### Personalização
Você pode modificar facilmente as seguintes configurações no código:
- `TAMANHO_GRADE`: Tamanho do campo (atual: 18x18)
- `NUM_BOMBAS`: Número de bombas (atual: 42)
- `TAMANHO_CELULA`: Tamanho de cada célula em pixels
- `CORES_NUMEROS`: Cores dos números de 1 a 8

## 🤝 Contribuindo

Contribuições são bem-vindas! Algumas ideias para melhorias:

### Funcionalidades Sugeridas
- [ ] Diferentes níveis de dificuldade
- [ ] Sistema de cronômetro
- [ ] Recordes pessoais
- [ ] Efeitos sonoros
- [ ] Animações de transição
- [ ] Temas personalizáveis

### Como Contribuir
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 🐛 Troubleshooting

### Problemas Comuns

**"ModuleNotFoundError: No module named 'pygame'"**
- Solução: Instale o Pygame usando `pip install pygame`

**Jogo não inicia ou tela preta**
- Verifique se o Pygame está instalado corretamente
- Tente executar com `python3` em vez de `python`

**Performance lenta**
- Verifique se sua máquina atende aos requisitos mínimos
- Feche outros programas que consomem recursos

## 📊 Estatísticas do Jogo

- **Células Totais**: 324
- **Bombas**: 42
- **Células Seguras**: 282
- **Densidade de Bombas**: 13%
- **Probabilidade de Vitória**: Depende da habilidade do jogador

⭐ **Gostou do projeto? Deixe uma estrela!** ⭐
