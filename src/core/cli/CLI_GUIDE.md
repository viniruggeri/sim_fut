# Interface CLI - Simulador de Futebol FIFA 25

## 🚀 Como usar a CLI

O simulador agora possui uma interface de linha de comando completa e interativa!

### Métodos de Execução

#### 1. **Windows (Recomendado)**
```batch
# Modo interativo completo
cli.bat

# Simulação rápida
cli.bat --quick --league serie_a --type simple

# Ver ajuda
cli.bat --help
```

#### 2. **Python Direto**
```bash
# Modo interativo
python cli.py --interactive

# Simulação rápida
python cli.py --quick --league premier_league --type advanced

# Listar ligas
python cli.py --list-leagues

# Ver ajuda
python cli.py --help
```

### 📋 Funcionalidades da CLI

#### **Modo Interativo** (`--interactive` ou sem argumentos)
- Menu principal com navegação intuitiva
- Seleção de liga visual
- Opções de simulação completas
- Visualização de resultados anteriores
- Configurações do sistema
- Limpeza de arquivos antigos

#### **Modo Rápido** (`--quick`)
- Execução direta sem menus
- Ideal para automação e scripts
- Suporte a todos os parâmetros

### 🎯 Argumentos Disponíveis

| Argumento | Descrição | Exemplo |
|-----------|-----------|---------|
| `--interactive`, `-i` | Modo interativo com menus | `cli.bat -i` |
| `--quick`, `-q` | Simulação rápida | `cli.bat -q` |
| `--league`, `-l` | Liga específica | `--league bundesliga` |
| `--type`, `-t` | Tipo de simulação | `--type advanced` |
| `--list-leagues` | Lista ligas disponíveis | `cli.bat --list-leagues` |
| `--help`, `-h` | Mostra ajuda | `cli.bat --help` |

### 🏆 Ligas Suportadas

1. **premier_league** - Premier League (Inglaterra)
2. **la_liga** - La Liga (Espanha) 
3. **serie_a** - Serie A (Itália)
4. **bundesliga** - Bundesliga (Alemanha)
5. **ligue_1** - Ligue 1 (França)

### 🔧 Tipos de Simulação

#### **Simple** (`--type simple`)
- Simulação estatística rápida
- Baseada em overalls dos times
- Resultados em CSV/JSON
- Tempo: ~5-10 segundos

#### **Advanced** (`--type advanced`)
- Simulação completa com jogadores individuais
- Estatísticas detalhadas (gols, assistências)
- Rankings de artilheiros
- Dados completos exportados
- Tempo: ~30-60 segundos

### 📁 Estrutura de Resultados

Os resultados são salvos em `data/processed/resultados/[liga]/`:

```
resultados_[liga]_[timestamp].csv    # Tabela final
resultados_[liga]_[timestamp].json   # Dados completos
resultados_[liga]_[timestamp]_tabela.csv      # (apenas advanced)
resultados_[liga]_[timestamp]_jogadores.csv   # (apenas advanced)
```

### 💡 Exemplos Práticos

#### Simulação Simples da Premier League
```batch
cli.bat --quick --league premier_league --type simple
```

#### Simulação Avançada do Brasileirão
```batch
cli.bat --quick --league serie_a --type advanced
```

#### Modo Interativo (Recomendado)
```batch
cli.bat
```
No modo interativo você pode:
- Escolher liga visualmente
- Ver resultados anteriores
- Limpar arquivos antigos
- Configurar sistema

#### Automação
```batch
# Script para simular todas as ligas
for %%L in (premier_league la_liga serie_a bundesliga ligue_1) do (
    cli.bat --quick --league %%L --type advanced
)
```

### 🐛 Resolução de Problemas

#### Erro de encoding (emojis)
✅ **Resolvido!** - Sistema usa apenas ASCII no Windows

#### CLI não encontra módulos
```batch
cd C:\Users\rugge_p2gkz2r\Desktop\python\sim_fut
pip install -r requirements.txt
```

#### Dados não encontrados
- Verifique se existe `config/config.yaml`
- Verifique se existe `data/processed/leagues/*.json`

### 🎮 Interface Interativa

Quando executar `cli.bat` (modo interativo), você verá:

```
================================================================================
                ⚽ SIMULADOR DE FUTEBOL FIFA 25 ⚽
                    Sistema de Linha de Comando
================================================================================
Liga atual: Premier League
Ligas disponíveis: 5
--------------------------------------------------------------------------------

[MENU PRINCIPAL]
1. Executar Simulação
2. Configurar Liga  
3. Ver Resultados Anteriores
4. Configurações do Sistema
5. Informações do Sistema
0. Sair
```

### 🚀 Vantagens da CLI

✅ **Rápida** - Execução direta sem carregar interface web  
✅ **Completa** - Todos os recursos disponíveis  
✅ **Interativa** - Menus intuitivos e navegação fácil  
✅ **Automação** - Suporte a scripts e batch  
✅ **Windows-First** - Otimizada para Windows com .bat  
✅ **Resultados Organizados** - Visualização e limpeza de histórico  

### 🔄 Integração

A CLI funciona perfeitamente junto com:
- 🌐 Interface Web (Streamlit)
- 🐳 Containers Docker  
- 📊 Scripts de análise
- 🛠️ Sistema de configuração existente

Agora você pode escolher usar via web OU via CLI! 🎉