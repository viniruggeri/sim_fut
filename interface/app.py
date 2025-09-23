import streamlit as st
import pandas as pd
import subprocess
import pathlib
import json
from config.config import config

st.set_page_config(page_title="Simulador de Ligas", layout="wide")

st.title("⚽ Simulador de Ligas Europeias")

# Selecionar liga
available = config["available_leagues"]
league = st.selectbox("Escolha a liga para simulação:", available)

# Selecionar modo
mode = st.radio("Modo de simulação:", ["Simple", "Advanced"])

# Botão de rodar simulação
if st.button("Rodar Simulação 🚀"):
    sim_file = "simple_sim.py" if mode == "Simple" else "advanced_sim.py"

    st.info(f"Rodando {mode} para a liga: {league}...")

    # Rodar via subprocess
    result = subprocess.run(
        ["python", sim_file],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        st.error("Erro na simulação!")
        st.text(result.stderr)
    else:
        st.success("Simulação concluída com sucesso!")
        st.text(result.stdout)

        # Buscar último arquivo salvo
        results_path = pathlib.Path(config["paths"]["results"]) / league
        json_files = sorted(results_path.glob("*.json"), reverse=True)
        
        if json_files:
            latest_file = json_files[0]
            with open(latest_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            df = pd.DataFrame(data["tabela_final"])
            st.dataframe(df, use_container_width=True)

            st.download_button(
                label="⬇️ Baixar Resultados (CSV)",
                data=df.to_csv(sep=";", index=False).encode("utf-8"),
                file_name=f"resultados_{league}.csv",
                mime="text/csv"
            )
