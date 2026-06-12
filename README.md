# Sistema de Análise Espaço-Temporal do Comportamento Tático no Futebol

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
Mede a **largura normalizada da linha defensiva** — razão entre o espaço lateral coberto pelos 4 defensores e a largura total do campo.
- Valor em [0, 1]: quanto maior, mais esticada e exposta a linha
- Cada segmento entre defensores adjacentes é monitorado individualmente: distâncias acima de **8 metros** são destacadas em vermelho, sinalizando um buraco na linha

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
│  Processamento      │  Pandas + NumPy
│  de Dados           │  Entidades: Frame · Bola · Jogador
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Visualização       │  Streamlit + Plotly
│                     │  Animação nativa frame a frame
└─────────────────────┘
```

### Tecnologias Utilizadas
| Camada | Tecnologia | Função |
|---|---|---|
| Ingestão | Python + [Kloppy](https://github.com/PySport/kloppy) | Leitura e normalização dos dados de tracking |
| Processamento | Pandas + NumPy | DataFrames e cálculo de métricas geométricas |
| Interface | Streamlit | Dashboard interativo com controles e camadas |
| Visualização | Plotly (`go.Frame`) | Animação 2D nativa com slider e play/pause |

---

## 🎨 Visualização

A interface 2D é composta por camadas ativáveis individualmente:

- **Botões (Jogadores):** Círculos identificados por cores e números (ID do jogador), com velocidade no hover
- **Campo:** Retângulo normalizado seguindo as proporções oficiais da FIFA
- **Esqueleto Tático:** Linhas dinâmicas conectando jogadores — a distensão indica perda de coesão
- **Shape Graph (Delaunay):** Triangulação sobre os jogadores, revelando conexões táticas instantâneas
- **Polígono Convexo (Hull):** Área ocupada pelo time em cada frame
- **Linhas de Formação:** Detecção automática das três linhas táticas (defesa, meio, ataque) com formação inferida (ex: 4-3-3)
- **Linha Defensiva:** Segmento conectando os defensores ordenados lateralmente — segmentos com distância superior a 8m ficam vermelhos, indicando buracos na linha
- **Stretch Index:** Índice de largura da linha defensiva exibido em tempo real na legenda, atualizado frame a frame

A visualização simplificada **"limpa" o ruído** das transmissões convencionais, permitindo ao treinador avaliar a geometria do time sem o viés da bola e validar se instruções táticas do treino estão sendo executadas em situações reais de jogo.

---

## Primeiros Passos

### Requisitos

- Python **3.12.2**
- Git

---

### 1. Criar o ambiente virtual

```bash
python3.12 -m venv .venv
```

> Se tiver múltiplas versões de Python instaladas, confirme a versão com:
> ```bash
> python3.12 --version
> ```

---

### 2. Ativar o ambiente virtual

**Windows:**
```bash
source .venv/Scripts/activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

O terminal deve mostrar `(.venv)` no início da linha.

---

### 3. Instalar as dependências

**Opção A — script de instalação (recomendado):**
```bash
./setup/setup.sh
```

**Opção B — pip direto (caso o script falhe):**
```bash
pip install -r requirements.txt
```

**Opção C — instalação manual (caso o requirements.txt falhe):**
```bash
pip install streamlit pandas numpy plotly kloppy
```

---

### 4. Rodar o app

```bash
python -m streamlit run src/app.py
```

---

### Problemas comuns

**`python3.12` não encontrado:**
Baixe em [python.org/downloads](https://www.python.org/downloads/release/python-3122/) e marque "Add to PATH" na instalação.

**Erro de permissão no setup.sh (macOS/Linux):**
```bash
chmod +x setup/setup.sh
./setup/setup.sh
```

**Dependências com conflito:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```