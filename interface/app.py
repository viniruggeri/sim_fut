import streamlit as st
import pandas as pd
import subprocess
import pathlib
import json
import sys
import os
from pathlib import Path

# Adicionar src ao path para imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

try:
    from config.config import config
except ImportError:
    # Fallback se config não estiver disponível
    config = {
        "paths": {
            "results": "./data/processed/resultados/"
        }
    }

st.set_page_config(page_title="Simulador de Ligas", layout="wide")

st.title("⚽ Simulador de Ligas Europeias")
st.markdown("**Sistema integrado de simulação de futebol com dados FIFA 25**")

# Ligas disponíveis (hardcoded por agora, mas funcional)
available_leagues = [
    "premier_league",
    "la_liga", 
    "bundesliga",
    "serie_a",
    "ligue_1"
]

# Interface principal
col1, col2 = st.columns(2)

with col1:
    league = st.selectbox(
        "🏆 Escolha a liga para simulação:", 
        available_leagues,
        format_func=lambda x: x.replace("_", " ").title()
    )

with col2:
    mode = st.radio("🎮 Modo de simulação:", ["Avançado", "Simples"])

st.markdown("---")

# Botão de simulação
if st.button("🚀 Rodar Simulação", type="primary", use_container_width=True):
    
    with st.spinner(f"🏟️ Simulando {league.replace('_', ' ').title()} no modo {mode}..."):
        
        try:
            if mode == "Avançado":
                # Usar o script de temporada completa que sabemos que funciona
                script_path = Path(__file__).parent.parent / "scripts" / "run_season_simulation.py"
                
                # Executar simulação avançada com liga selecionada
                result = subprocess.run(
                    [sys.executable, str(script_path), "--league", league],
                    capture_output=True,
                    text=True,
                    cwd=str(Path(__file__).parent.parent)
                )
                
            else:
                # Simulação simples
                script_path = Path(__file__).parent.parent / "src" / "core" / "simple" / "simulator.py"
                
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True, 
                    text=True,
                    cwd=str(Path(__file__).parent.parent)
                )

            if result.returncode != 0:
                st.error("❌ Erro na simulação!")
                st.code(result.stderr, language="bash")
                st.code(result.stdout, language="text")
            else:
                st.success("✅ Simulação concluída com sucesso!")
                
                # Mostrar output em expander
                with st.expander("📋 Log da Simulação"):
                    st.text(result.stdout)

                # Buscar últimos resultados
                results_base = Path(config["paths"]["results"]) 
                results_path = results_base / league
                
                if results_path.exists():
                    # Buscar arquivos JSON mais recentes
                    json_files = sorted(results_path.glob("*.json"), reverse=True)
                    
                    if json_files:
                        latest_file = json_files[0]
                        
                        try:
                            with open(latest_file, "r", encoding="utf-8") as f:
                                data = json.load(f)

                            # Exibir resumo
                            st.markdown("## 📊 Resultados da Simulação")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("🏆 Campeão", data["summary"]["champion"])
                            with col2:
                                st.metric("⚽ Total de Gols", data["summary"]["total_goals"])
                            with col3:
                                st.metric("🎯 Artilheiro", data["summary"]["top_scorer"])
                            with col4:
                                st.metric("🥅 Gols do Artilheiro", data["summary"]["top_scorer_goals"])

                            # Tabela da liga
                            st.markdown("### 🏆 Tabela Final")
                            df_table = pd.DataFrame(data["tabela_final"])
                            
                            # Renomear colunas para melhor exibição
                            df_table = df_table.rename(columns={
                                'Time': '🏟️ Time',
                                'J': 'J',
                                'V': 'V', 
                                'E': 'E',
                                'D': 'D',
                                'GP': 'GP',
                                'GC': 'GC', 
                                'SG': 'SG',
                                'P': '📊 Pts'
                            })
                            
                            st.dataframe(df_table, use_container_width=True, hide_index=True)

                            # Top artilheiros
                            if "top_10_artilheiros" in data:
                                st.markdown("### ⚽ Top 10 Artilheiros")
                                df_scorers = pd.DataFrame(data["top_10_artilheiros"])
                                df_scorers_display = df_scorers[['Nome', 'Time', 'Gols', 'Jogos']].head(10)
                                st.dataframe(df_scorers_display, use_container_width=True, hide_index=True)

                            # Botões de download
                            st.markdown("### 💾 Downloads")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                csv_data = df_table.to_csv(sep=";", index=False).encode("utf-8")
                                st.download_button(
                                    label="📊 Baixar Tabela (CSV)",
                                    data=csv_data,
                                    file_name=f"tabela_{league}_{data['created_at'][:10]}.csv",
                                    mime="text/csv"
                                )
                            
                            with col2:
                                json_data = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
                                st.download_button(
                                    label="📋 Baixar Completo (JSON)", 
                                    data=json_data,
                                    file_name=f"simulacao_{league}_{data['created_at'][:10]}.json",
                                    mime="application/json"
                                )

                        except Exception as e:
                            st.error(f"❌ Erro ao carregar resultados: {e}")
                    else:
                        st.warning("⚠️ Nenhum resultado encontrado!")
                else:
                    st.warning("⚠️ Pasta de resultados não encontrada!")
                    
        except Exception as e:
            st.error(f"❌ Erro inesperado: {e}")
            st.exception(e)

# Rodapé
st.markdown("---")
st.markdown("🎮 **Simulador de Futebol Avançado** | Dados FIFA 25 | Desenvolvido com ❤️")
