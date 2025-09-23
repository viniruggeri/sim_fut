# ⚽ Simulador de Futebol FIFA 25

Um simulador completo de campeonatos de futebol baseado nos dados reais do FIFA 25, oferecendo desde simulações simples até um sistema avançado com evolução de jogadores, táticas e estatísticas detalhadas.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg)](https://github.com/viniruggeri/sim_fut)
[![GitHub](https://img.shields.io/badge/GitHub-viniruggeri-181717.svg)](https://github.com/viniruggeri)

> 🎯 **Projeto Pessoal** - Desenvolvido por hobby e aprendizado, sem fins lucrativos

## ✨ Visão Geral

Este projeto oferece **dois sistemas de simulação**:

- **🏃‍♂️ Sistema Simples**: Simulações rápidas baseadas em médias dos times
- **🧠 Sistema Avançado**: Simulações detalhadas com evolução de jogadores, formações táticas e estatísticas avançadas *(em desenvolvimento)*

## 📁 Estrutura do Projeto

```text
sim_fut/
├── 📂 config/
│   ├── config.yaml                 # Configurações principais
│   └── config.example.yaml         # Exemplo de configuração
├── 📂 data/
│   ├── raw/
│   │   └── fifa25_players.csv      # Dataset FIFA 25 (18k+ jogadores)
│   └── processed/
│       └── resultados/             # Resultados das simulações
├── 📂 json_ligas/                  # Dados processados das ligas
│   ├── premier_league_2025.json
│   ├── la_liga_2025.json
│   ├── serie_a_2025.json
│   ├── bundesliga_2025.json
│   └── ligue_1_2025.json
├── 📂 src/
│   ├── core/
│   │   ├── simple/                 # Sistema de simulação simples
│   │   └── advanced/               # Sistema avançado (🚧 em desenvolvimento)
│   │       ├── models/             # Modelos de dados avançados
│   │       ├── simulation/         # Motor de simulação complexo
│   │       ├── statistics/         # Stats avançadas (xG, xA, etc.)
│   │       └── tactics/            # Sistema de formações e táticas
│   └── utils/
│       └── config.py               # Gerenciamento de configurações
├── 📂 interface/
│   └── app.py                      # Interface Streamlit (futuro)
├── 📂 scripts/
│   ├── processCSV.py               # Processamento do dataset
│   └── run_advanced.py             # Simulação avançada (futuro)
├── simple_sim.py                   # Simulador atual
├── requirements.txt
└── README.md
```

## 🚀 Funcionalidades Atuais

### 🏃‍♂️ Sistema Simples

#### 📊 Processamento de Dados
- **Dataset FIFA 25**: Mais de 18.000 jogadores processados
- **Top 5 Ligas Europeias**:
  - 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (ID: 13)
  - 🇪🇸 La Liga (ID: 53) 
  - 🇮🇹 Serie A (ID: 31)
  - 🇩🇪 Bundesliga (ID: 19)
  - 🇫🇷 Ligue 1 (ID: 16)
- **Classificação por Setores**: Ataque, Meio, Defesa, Goleiro
- **Médias por Time**: Calculadas automaticamente por setor

#### ⚽ Motor de Simulação
- **Algoritmo**: Distribuição de Poisson baseada em força dos times
- **Fatores Configuráveis**:
  - Aleatoriedade: 0.5 - 1.5 (configurável)
  - Gols mínimos esperados: 0.1 (evita zeros absolutos)
  - Seed para reproduzibilidade
- **Sistema de Pontuação**: Tabela completa com estatísticas
- **Configuração YAML**: Todas as opções centralizadas

### 🧠 Sistema Avançado *(🚧 Em Desenvolvimento)*

#### 🎮 Funcionalidades Planejadas
- **Evolução de Jogadores**: Overall → Potential ao longo da temporada
- **Sistema de Formações**: 4-4-2, 4-3-3, 4-2-3-1, etc.
- **Escalações Realistas**: Apenas 11 jogadores por time
- **Estatísticas Avançadas**:
  - xG (Expected Goals) e xA (Expected Assists)
  - Stats por 90 minutos
  - Gols, assistências, finalizações
- **Sistema de Lesões**: Jogadores podem se lesionar
- **Fadiga e Moral**: Afetam performance
- **Substituições Táticas**: Durante as partidas

#### 📈 Dados Avançados
- **Atributos Detalhados**: Pace, shooting, passing, dribbling, etc.
- **Posições Múltiplas**: Jogadores podem atuar em várias posições
- **Tracking Temporal**: Histórico de evolução e performance
- **Análise Tática**: Formações e estratégias por time

## 📊 Estrutura dos Dados

### Jogadores (Sistema Simples)

```json
{
  "nome_jogador": {
    "overall": 85,
    "potential": 89,
    "altura_cm": 180,
    "peso_kg": 75,
    "foto": "url_da_foto",
    "playstyles": ["Dribbler", "Clinical finisher"],
    "setor": "Ataque"
  }
}
```

### Times (Sistema Simples)

```json
{
  "nome_time": {
    "medias": {
      "ataque": 78.5,
      "meio": 76.2, 
      "defesa": 74.8,
      "goleiro": 81.0
    },
    "jogadores": { /* ... */ }
  }
}
```

### Jogadores (Sistema Avançado - Futuro)

```json
{
  "player_id": "uuid",
  "name": "Lionel Messi",
  "age": 36,
  "position": "RW",
  "current_overall": 91,
  "potential": 91,
  "attributes": {
    "pace": 85,
    "shooting": 92,
    "passing": 95,
    "dribbling": 95
  },
  "season_stats": {
    "goals": 25,
    "assists": 15,
    "xg": 22.5,
    "xa": 18.2,
    "goals_per_90": 0.85
  }
}
```

## ⚙️ Instalação e Configuração

### 📋 Pré-requisitos

```bash
# Python 3.12+ recomendado
python --version

# Dependências principais
pip install pandas numpy pyyaml
```

### 🔧 Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/viniruggeri/sim_fut.git
   cd sim_fut
   ```

2. **Instale dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o ambiente**
   ```bash
   cp config/config.example.yaml config/config.yaml
   # Edite config/config.yaml conforme necessário
   ```

### ⚡ Configuração

#### `config/config.yaml`

```yaml
# Liga a simular
league: premier_league

# Caminhos
paths:
  data: ./data/
  json_ligas: ./json_ligas/
  results: ./resultados/

# Configurações de simulação
simulation:
  double_round: true
  random_factor_min: 0.5
  random_factor_max: 1.5
  seed: 42  # Para reproduzibilidade (null = aleatório)
  min_expected_goals: 0.1

# Output
output:
  csv_separator: ";"
  timestamp_format: "%Y-%m-%d_%H-%M-%S"
  csv_include_index: false

# Logging
logging:
  level: INFO
```

## 🎯 Como Usar

### 1. Processamento dos Dados

```bash
python scripts/processCSV.py
```

**O que faz:**

- Processa o arquivo `data/raw/fifa25_players.csv`
- Gera arquivos JSON para cada liga em `json_ligas/`
- Calcula médias por setor para cada time

### 2. Simulação Simples

```bash
python simple_sim.py
```

**O que faz:**

- Simula uma temporada completa da liga configurada
- Gera tabela de classificação final
- Salva resultados em CSV e JSON com timestamp

### 3. Mudar Liga

Edite `config/config.yaml`:

```yaml
league: la_liga  # ou premier_league, serie_a, bundesliga, ligue_1
```

## 📊 Formato dos Resultados

### Tabela CSV

```csv
Time;P;V;E;D;GP;GC;SG
Manchester City;98;32;2;4;89;23;66
Arsenal;87;28;3;7;84;35;49
Chelsea;84;27;3;8;82;39;43
...
```

### Arquivo JSON

```json
{
  "version": "1.0.0",
  "created_at": "2025-09-23_01-25-28",
  "hash": "sha256:cb32999b026...",
  "tabela_final": [
    {
      "index": "Manchester City",
      "P": 98,
      "V": 32,
      "E": 2,
      "D": 4,
      "GP": 89,
      "GC": 23,
      "SG": 66
    }
  ]
}
```

### Legenda das Estatísticas

- **P**: Pontos (3 por vitória, 1 por empate)
- **V**: Vitórias
- **E**: Empates
- **D**: Derrotas
- **GP**: Gols Pró (marcados)
- **GC**: Gols Contra (sofridos)
- **SG**: Saldo de Gols (GP - GC)

## � Algoritmo de Simulação

### Sistema Simples

1. **Expectativa de Gols**: `exp_goals = (ataque_time / defesa_adversario) / fator_aleatorio`
2. **Distribuição de Poisson**: Gera número de gols baseado na expectativa
3. **Fator de Aleatoriedade**: Configurável (padrão: 0.5 - 1.5)
4. **Proteção Mínima**: Evita expectativas zero (mín. 0.1 gols)
5. **Reproduzibilidade**: Seed configurável para resultados consistentes

### Sistema Avançado *(Futuro)*

- **xG/xA**: Expected Goals e Expected Assists por chance criada
- **Posições Reais**: Formações táticas respeitadas
- **Evolução**: Jogadores crescem durante a temporada
- **Fatores Contextuais**: Lesões, fadiga, moral afetam performance

## 📈 Performance e Escalabilidade

- **Processamento**: ~18.000 jogadores em segundos
- **Simulação Simples**: Temporada completa (380 jogos) instantânea
- **Memória**: Otimizada com pandas e numpy
- **Armazenamento**: JSONs compactos com hash de integridade
- **Logging**: Rastreamento completo com níveis configuráveis

## 🚧 Roadmap de Desenvolvimento

### ✅ Concluído
- [x] Sistema de simulação simples
- [x] Configuração centralizada (YAML)
- [x] Processamento dataset FIFA 25
- [x] Top 5 ligas europeias
- [x] Logging estruturado
- [x] Resultados em CSV/JSON

### 🚧 Em Desenvolvimento
- [ ] **Sistema Avançado**
  - [ ] Modelos de dados complexos
  - [ ] Sistema de formações (4-4-2, 4-3-3, etc.)
  - [ ] Evolução de jogadores
  - [ ] Estatísticas avançadas (xG, xA)
  - [ ] Sistema de lesões e fadiga

### 🔮 Futuro
- [ ] Interface web (Streamlit)
- [ ] API REST
- [ ] Sistema de transferências
- [ ] Análise de desempenho tático
- [ ] Comparação entre temporadas
- [ ] Exportação para dashboards
- [ ] Machine Learning para predições

## 🔧 Desenvolvimento

### Estrutura para Contribuições

```bash
# Para desenvolvimento do sistema avançado
src/core/advanced/
├── models/         # Classes Player, Team, Match
├── simulation/     # Motor de simulação complexo
├── statistics/     # Cálculo de métricas avançadas
└── tactics/        # Sistema de formações

# Para testes
tests/
├── test_simple_simulation.py
├── test_data_processing.py
└── test_advanced_features.py
```

### Executar Testes

```bash
python -m pytest tests/ -v
```

## 📝 Requisitos do Dataset

O `fifa25_players.csv` deve conter:

- `club_name`: Nome do clube
- `club_league_id`: ID da liga (13, 53, 31, 19, 16)
- `overall_rating`: Rating geral do jogador
- `potential`: Potencial máximo
- `positions`: Posições que o jogador pode jogar
- `name`: Nome completo do jogador
- Metadados: altura, peso, foto, playstyles, etc.

## 🤝 Contribuindo

1. Fork o projeto no [GitHub](https://github.com/viniruggeri/sim_fut)
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

**Nota**: Este é um projeto pessoal desenvolvido para fins educacionais e de hobby, sem intenções comerciais ou fins lucrativos.

## 🙏 Agradecimentos

- **EA Sports** pelos dados do FIFA 25
- **Comunidade Python** pelas bibliotecas fantásticas
- **Desenvolvedores** que contribuem com o projeto

## 👨‍💻 Autor

**Vinicius Ruggeri** - [@viniruggeri](https://github.com/viniruggeri)

> 💡 Projeto desenvolvido por paixão ao futebol e programação

---

Desenvolvido com ⚽ e dados reais do FIFA 25
