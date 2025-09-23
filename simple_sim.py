import numpy as np
import pandas as pd
import json
import datetime
import hashlib
import pathlib
from config.config import config, logger

# Configurações do YAML
LEAGUE = config["league"]
PATHS = config["paths"]
SIM_CONFIG = config["simulation"]
OUTPUT_CONFIG = config["output"]

logger.info(f"Iniciando simulação para a liga: {LEAGUE}")
logger.info(f"Configurações de simulação: {SIM_CONFIG}")

# Configurar seed para reproduzibilidade
if SIM_CONFIG.get("seed"):
    np.random.seed(SIM_CONFIG["seed"])
    logger.info(f"Seed configurada: {SIM_CONFIG['seed']}")

# Construir caminhos baseados na configuração
subdir = LEAGUE.replace(" ", "_").lower()
RESULTS_PATH = f"{PATHS['results']}{subdir}"

today = datetime.datetime.now().strftime(OUTPUT_CONFIG["timestamp_format"])

# carregar JSON de times
json_file_path = f"{PATHS['json_ligas']}{LEAGUE}_2025.json"
logger.info(f"Carregando dados de: {json_file_path}")
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# pegar os times já com as médias
times = {nome: {"ataque": info["medias"]["ataque"], "defesa": info["medias"]["defesa"]}
         for nome, info in data["times"].items()}

def sim_game(timeA, timeB):
    atkA, defA = times[timeA]["ataque"], times[timeA]["defesa"]
    atkB, defB = times[timeB]["ataque"], times[timeB]["defesa"]

    # Usar fatores aleatórios configuráveis
    fator = np.random.uniform(
        SIM_CONFIG["random_factor_min"], 
        SIM_CONFIG["random_factor_max"]
    )
    exp_a = max(SIM_CONFIG["min_expected_goals"], (atkA / defB) / fator)
    exp_b = max(SIM_CONFIG["min_expected_goals"], (atkB / defA) / fator)

    gols_a = np.random.poisson(exp_a)
    gols_b = np.random.poisson(exp_b)
    return gols_a, gols_b


def sim_campeonato(times_dict):
    logger.info(f"Iniciando simulação do campeonato com {len(times_dict)} times")
    tabela = {t: {"P": 0, "V": 0, "E": 0, "D": 0, "GP": 0, "GC": 0, "SG": 0} for t in times_dict}
    
    total_jogos = len(times_dict) * (len(times_dict) - 1)
    jogos_simulados = 0

    for i, timeA in enumerate(times_dict):
        for j, timeB in enumerate(times_dict):
            if i != j:
                gA, gB = sim_game(timeA, timeB)
                jogos_simulados += 1

                tabela[timeA]["GP"] += gA
                tabela[timeA]["GC"] += gB
                tabela[timeB]["GP"] += gB
                tabela[timeB]["GC"] += gA

                if gA > gB:
                    tabela[timeA]["P"] += 3
                    tabela[timeA]["V"] += 1
                    tabela[timeB]["D"] += 1
                elif gB > gA:
                    tabela[timeB]["P"] += 3
                    tabela[timeB]["V"] += 1
                    tabela[timeA]["D"] += 1
                else:
                    tabela[timeA]["P"] += 1
                    tabela[timeB]["P"] += 1
                    tabela[timeA]["E"] += 1
                    tabela[timeB]["E"] += 1

    for t in tabela:
        tabela[t]["SG"] = tabela[t]["GP"] - tabela[t]["GC"]

    logger.info(f"Simulação concluída: {jogos_simulados} jogos simulados")
    df = pd.DataFrame(tabela).T
    df = df.sort_values(by=["P", "V", "SG", "GP"], ascending=[False, False, False, False])
    return df


# rodar 1 temporada
logger.info("Iniciando simulação da temporada")
df_final = sim_campeonato(times)

# gerar hash (SHA256) do dataframe como string
hash_value = hashlib.sha256(df_final.to_json().encode()).hexdigest()

# empacotar tudo em JSON
output = {
    "version": "1.0.0",
    "created_at": today,
    "hash": f"sha256:{hash_value}",
    "tabela_final": df_final.reset_index().to_dict(orient="records"),
}

# salvar CSV e JSON
logger.info(f"Salvando resultados em: {RESULTS_PATH}")
pathlib.Path(RESULTS_PATH).mkdir(parents=True, exist_ok=True)

csv_path = pathlib.Path(RESULTS_PATH) / f"resultados_{LEAGUE}_{today}.csv"
json_path = pathlib.Path(RESULTS_PATH) / f"resultados_{LEAGUE}_{today}.json"

df_final.to_csv(csv_path, sep=OUTPUT_CONFIG["csv_separator"], index=OUTPUT_CONFIG["csv_include_index"])
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

logger.info("Simulação concluída com sucesso!")
print(df_final)
print(f"\nResultados salvos em:\n{csv_path}\n{json_path}")