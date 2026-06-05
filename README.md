# 🏟️ ButtonTactics Pro (BTP)
### Sistema de Análise Espaço-Temporal do Comportamento Tático no Futebol

> **Trabalho do Grau A (TGA) — Tópicos Especiais em Computação (Computação Aplicada ao Futebol)**
> Universidade do Vale do Rio dos Sinos — Unisinos

---

## 🎯 Definição do Problema

No cenário contemporâneo do futebol de alto rendimento, métricas tradicionais baseadas em **eventos isolados** falham em capturar a dinâmica estrutural de uma equipe — como a manutenção da compactação defensiva, a velocidade de recomposição e a integridade das linhas táticas sob pressão.

A ausência de ferramentas acessíveis que traduzam coordenadas espaciais em **insights geométricos** dificulta a tomada de decisão técnica e a identificação precoce de falhas estruturais. Existe também uma lacuna significativa na detecção em tempo real de **falhas de compactação** e do fenômeno de **deriva tática** — a perda progressiva de posicionamento causada por fadiga ou pressão adversária.

O **ButtonTactics Pro** surge para resolver este problema: em vez de tratar jogadores como pontos isolados, o sistema monitora a **integridade estrutural da equipe como uma unidade tática coesa**, baseando-se em conectividade e modelos geométricos.

---

## 🚀 Proposta de Solução

O sistema converte dados de rastreamento posicional (tracking data) em uma interface de suporte à decisão técnica com visualização inspirada na estética clássica do **jogo de botão** — uma simulação 2D em plano cartesiano que elimina o ruído visual das transmissões convencionais e entrega uma **percepção geométrica instantânea** da partida para treinadores e analistas.

---

## 📊 Métricas e Análises

### 🔺 Grafos de Forma (Shape Graphs)
Utiliza a **Triangulação de Delaunay** para mapear conexões táticas instantâneas sem depender de formações nominais estáticas (4-4-2, 4-3-3 etc.).
- Em cada frame, constrói-se a triangulação sobre os 11 jogadores da equipe
- Extrai-se um subgrafo filtrando apenas as "arestas estáveis" que resistem a perturbações
- A ruptura repentina de arestas indica mudança de estrutura em tempo real

### 📏 Índice de Estiramento (Stretch Index)
Mede a **espessura e compactação da última linha defensiva**, avaliando simultaneamente a área do polígono convexo dos 4 defensores e a distância dos atacantes adversários mais próximos.
- Um aumento no índice indica perda de compactação no setor defensivo primário

### ⏱️ Tempo de Recomposição (Time-to-Shape)
Calcula o tempo exato entre o evento de **"Perda de Posse"** e o momento em que a equipe recupera sua geometria defensiva ideal.
- Identifica se o time é vulnerável a contra-ataques por demora na transição defensiva

### 📐 Deformação Geométrica (In vs. Out of Possession)
Analisa como a forma do time se altera conforme a posse de bola, medindo **Amplitude (Largura)** e **Profundidade (Comprimento)** médias.
- Times de alta performance expandem sua área em até 30% ao ganhar a posse
- Ausência dessa expansão indica falha de construção tática

### 🔍 Linhas Quebradas (Defensive Gaps)
Identifica buracos na estrutura tática calculando distâncias entre defensores. Se a distância entre Lateral e Zagueiro exceder um limite pré-definido (ex: 15m), o sistema emite um **"Gatilho de Risco"**.

### 😓 Deriva Tática (Drift)
Monitora a **altura média da linha defensiva** em blocos de 15 minutos. Uma queda progressiva sem substituições ou mudanças de formação configura deriva tática por exaustão física.

### 💪 Eficiência Defensiva por Compactação
Correlaciona a localização de cada bola roubada com o grau de compactação do time naquele instante, inferindo se o desarme foi fruto de ação individual ou de movimentação coletiva do bloco.

---

## 🛠️ Arquitetura e Tecnologias

O sistema segue um pipeline de dados estruturado em três camadas:

```
[Dados de Tracking]
      │
      ▼
┌─────────────────────┐
│  Ingestão           │  Python + Kloppy
│  & Padronização     │  Normalização de diferentes provedores
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Processamento      │  Pandas DataFrames
│  de Dados           │  Entidades: Frame · Bola · Jogador
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Visualização       │  HTML5 + JavaScript (Canvas)
│                     │  Simulação 2D estilo "jogo de botão"
└─────────────────────┘
```

### Tecnologias Utilizadas
| Camada | Tecnologia | Função |
|---|---|---|
| Ingestão | Python + [Kloppy](https://github.com/PySport/kloppy) | Leitura e normalização dos dados de tracking |
| Processamento | Pandas | DataFrames e cálculo massivo de métricas |
| Visualização | HTML5 Canvas + JavaScript | Renderização da simulação 2D e camadas auxiliares |

---

## 🎨 Visualização

A interface 2D é composta por camadas:

- **Botões (Jogadores):** Círculos identificados por cores e números (ID do jogador)
- **Campo:** Retângulo normalizado seguindo as proporções oficiais da FIFA
- **Esqueleto Tático:** Linhas dinâmicas conectando jogadores do mesmo setor — a distensão indica perda de coesão
- **Vetores de Deslocamento:** Setas indicando direção e intensidade do movimento no próximo frame
- **Gráfico de Compactação:** Painel lateral sincronizado mostrando a variação da distância entre as linhas defensiva e ofensiva ao longo do tempo

A visualização simplificada **"limpa" o ruído** das transmissões convencionais, permitindo ao treinador avaliar a geometria do time sem o viés da bola e validar se instruções táticas do treino estão sendo executadas em situações reais de jogo.

---

