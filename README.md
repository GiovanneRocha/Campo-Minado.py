# Campo Minado 💣

Um jogo clássico de Campo Minado implementado em Python, oferecendo uma experiência nostálgica e desafiadora para todos os níveis de jogadores.

## 📋 Descrição

O Campo Minado é um jogo de lógica onde o objetivo é limpar um campo minado sem detonar nenhuma mina. O jogador deve usar pistas numéricas para determinar onde as minas estão localizadas e marcar as células suspeitas. Este projeto implementa todas as funcionalidades clássicas do jogo com uma interface intuitiva.

### ✨ Funcionalidades

- **Interface Gráfica**: Interface amigável e responsiva
- **Múltiplos Níveis**: Iniciante, Intermediário e Avançado
- **Sistema de Marcação**: Marque células suspeitas com bandeiras
- **Contador de Minas**: Acompanhe quantas minas restam
- **Cronômetro**: Desafie-se a melhorar seus tempos
- **Reiniciar Jogo**: Comece uma nova partida a qualquer momento

## 🎮 Como Jogar

1. **Clique em uma célula** para revelá-la
2. **Números** indicam quantas minas estão nas células adjacentes
3. **Clique com o botão direito** para marcar/desmarcar uma célula como mina
4. **Objetivo**: Revelar todas as células que não contêm minas
5. **Cuidado**: Se clicar em uma mina, o jogo termina!

### 🎯 Níveis de Dificuldade

- **Iniciante**: 9x9 campo com 10 minas
- **Intermediário**: 16x16 campo com 40 minas  
- **Avançado**: 30x16 campo com 99 minas

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.6 ou superior
- Biblioteca Tkinter (geralmente incluída na instalação padrão do Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/GiovanneRocha/Campo-Minado.py.git
cd Campo-Minado.py
```

2. Verifique se possui o Python instalado:
```bash
python --version
```

3. Execute o jogo:
```bash
python campo_minado.py
```

### Execução Alternativa

Se você tiver problemas com `python`, tente:
```bash
python3 campo_minado.py
```

## 🎲 Instruções de Uso

### Controles do Mouse
- **Clique esquerdo**: Revela uma célula
- **Clique direito**: Marca/desmarca uma célula com bandeira
- **Clique duplo**: Revela células adjacentes (quando o número de bandeiras ao redor corresponde ao número da célula)

### Interface
- **Contador de Minas**: Mostra quantas minas restam para marcar
- **Cronômetro**: Exibe o tempo decorrido
- **Botão Reiniciar**: Inicia uma nova partida
- **Seletor de Dificuldade**: Escolha entre os níveis disponíveis

## 🏆 Estratégias e Dicas

- Comece pelas bordas e cantos do campo
- Use números para deduzir onde estão as minas
- Marque células que você tem certeza que contêm minas
- Procure por padrões comuns (1-2-1, 1-2-2-1, etc.)
- Quando em dúvida, use probabilidade para fazer a melhor escolha

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem principal
- **Tkinter**: Interface gráfica
- **Random**: Geração aleatória de posições das minas
- **Time**: Controle do cronômetro

## 📁 Estrutura do Projeto

```
Campo-Minado.py/
├── campo_minado.py          # Arquivo principal do jogo
├── README.md                # Este arquivo
└── assets/                  # Recursos do jogo (se aplicável)
    ├── icons/              # Ícones do jogo
    └── sounds/             # Sons do jogo (opcional)
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abrir um Pull Request

## 🐛 Problemas Conhecidos

- Liste aqui qualquer problema conhecido ou limitação do projeto

## 📋 Roadmap

- [ ] Adicionar sons e efeitos sonoros
- [ ] Implementar sistema de pontuação
- [ ] Adicionar modo multiplayer
- [ ] Criar temas personalizáveis
- [ ] Implementar salvamento de estatísticas

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Giovanne Rocha**
- GitHub: [@GiovanneRocha](https://github.com/GiovanneRocha)
- LinkedIn: [Seu LinkedIn](https://linkedin.com/in/seu-perfil)

## 🙏 Agradecimentos

- Inspirado no clássico jogo Campo Minado da Microsoft
- Agradecimentos especiais à comunidade Python
- Obrigado a todos que contribuíram com feedbacks e sugestões

---

⭐ **Gostou do projeto? Deixe uma estrela!** ⭐
