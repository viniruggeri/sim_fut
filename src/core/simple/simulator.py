#!/usr/bin/env python3
import sys
import os
import json
import argparse
import pathlib
import hashlib
import datetime
import logging
from pathlib import Path

import numpy as np
import pandas as pd

# Adicionar config ao path
config_path = Path(__file__).parent.parent.parent.parent / "config"
sys.path.insert(0, str(config_path))

import config

def sim_game(timeA, timeB, times, sim_config, casa=True):
    """Simula um jogo entre dois times"""
    # Calcular força ofensiva (ataque tem mais peso que meio)
    atkA = (times[timeA]["ataque"] * 0.7) + (times[timeA]["meio"] * 0.3)
    atkB = (times[timeB]["ataque"] * 0.7) + (times[timeB]["meio"] * 0.3)
    
    # Calcular força defensiva (defesa tem mais peso que goleiro)
    defA = (times[timeA]["defesa"] * 0.7) + (times[timeA]["goleiro"] * 0.3) 
    defB = (times[timeB]["defesa"] * 0.7) + (times[timeB]["goleiro"] * 0.3)
    
    # Bônus de mando de campo
    if casa:
        atkA *= 1.10  # 10% boost no ataque
        defA *= 1.05  # 5% boost na defesa
    
    # Usar fatores aleatórios configuráveis
    fator = np.random.uniform(
        sim_config["random_factor_min"], 
        sim_config["random_factor_max"]
    )
    
    # Calcular gols esperados
    divisor = 75  # Balanceamento
    exp_a = max(sim_config["min_expected_goals"], (atkA / defB) * (divisor/75) / fator)
    exp_b = max(sim_config["min_expected_goals"], (atkB / defA) * (divisor/75) / fator)

    gols_a = np.random.poisson(exp_a)
    gols_b = np.random.poisson(exp_b)
    return gols_a, gols_b


def sim_campeonato(times_dict, sim_config):
    """Simula um campeonato completo"""
    print(f"Iniciando simulação do campeonato com {len(times_dict)} times")
    
    tabela = {t: {"P": 0, "V": 0, "E": 0, "D": 0, "GP": 0, "GC": 0, "SG": 0} for t in times_dict}
    
    total_jogos = len(times_dict) * (len(times_dict) - 1)
    jogos_simulados = 0

    for i, timeA in enumerate(times_dict):
        for j, timeB in enumerate(times_dict):
            if i != j:
                # timeA joga em casa
                gA, gB = sim_game(timeA, timeB, times_dict, sim_config, casa=True)
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

    print(f"Simulação concluída: {jogos_simulados} jogos simulados")
    df = pd.DataFrame(tabela).T
    df = df.sort_values(by=["P", "V", "SG", "GP"], ascending=[False, False, False, False])
    return df


def main(league_override=None):
    """Função principal do simulador simples"""
    
    # Parse argumentos se chamado diretamente
    if league_override is None and len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Simulador Simples')
        parser.add_argument('--league', 
                           type=str, 
                           default=None,
                           help='Liga para simular')
        args = parser.parse_args()
        league_override = args.league
    
    # Determinar liga a usar
    if league_override:
        league = league_override
    elif os.getenv('LEAGUE'):
        league = os.getenv('LEAGUE')
    else:
        league = config.config["league"]
        
    # Obter configurações
    paths = config.config["paths"]
    sim_config = config.config["simulation"]
    output_config = config.config["output"]

    print(f"🚀 Iniciando simulação para a liga: {league}")
    print(f"Configurações de simulação: {sim_config}")

    # Configurar seed para reproduzibilidade
    if sim_config.get("seed"):
        np.random.seed(sim_config["seed"])
        print(f"Seed configurada: {sim_config['seed']}")

    # Construir caminhos baseados na configuração
    subdir = league.replace(" ", "_").lower()
    results_path = f"{paths['results']}{subdir}"
    today = datetime.datetime.now().strftime(output_config["timestamp_format"])

    # Carregar JSON de times
    json_file_path = f"{paths['json_ligas']}{league}_2025.json"
    print(f"Carregando dados de: {json_file_path}")
    
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Erro: Liga '{league}' não encontrada em {json_file_path}")
        return

    # Pegar os times já com as médias
    times = {nome: {
        "ataque": info["medias"]["ataque"], 
        "meio": info["medias"]["meio"],
        "defesa": info["medias"]["defesa"],
        "goleiro": info["medias"]["goleiro"]
    } for nome, info in data["times"].items()}

    print(f"Times carregados: {len(times)}")
    print("-" * 50)

    # Rodar simulação
    print("Iniciando simulação da temporada...")
    df_final = sim_campeonato(times, sim_config)

    # Gerar hash do resultado
    hash_value = hashlib.sha256(df_final.to_json().encode()).hexdigest()

    # Criar JSON completo
    output_data = {
        "version": "1.0.0",
        "simulation_type": "simple",
        "created_at": today,
        "league": league,
        "tabela_final": df_final.to_dict(orient="records"),
        "hash": f"sha256:{hash_value}"
    }

    # Salvar resultados
    print(f"Salvando resultados em: {results_path}")
    pathlib.Path(results_path).mkdir(parents=True, exist_ok=True)

    csv_path = pathlib.Path(results_path) / f"resultados_{league}_{today}.csv"
    json_path = pathlib.Path(results_path) / f"resultados_{league}_{today}.json"

    df_final.to_csv(csv_path, sep=output_config["csv_separator"], 
                   index=output_config["csv_include_index"], encoding="utf-8")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    # Mostrar tabela na tela
    print(df_final)
    print(f"\nResultados salvos em:")
    print(f"{csv_path}")
    print(f"{json_path}")
    print("✅ Simulação concluída!")


if __name__ == "__main__":
    main()