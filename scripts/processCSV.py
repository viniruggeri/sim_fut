import pandas as pd
import json
from datetime import datetime
import hashlib
import pathlib

# carrega dataset
df = pd.read_csv("./data/fifa25_players.csv")
df = df.dropna(subset=["club_name", "overall_rating"])

# set de ligas top 5
top5_leagues = {
    13: "premier_league",
    53: "la_liga",
    31: "serie_a",
    19: "bundesliga",
    16: "ligue_1"
}

# classificação por setor
attack_pos = {"ST","CF","RW","LW","LF","RF"}
mid_pos    = {"CM","CAM","CDM","LM","RM"}
def_pos    = {"CB","LB","RB","RWB","LWB"}
gk_pos     = {"GK"}

def classify_sector(positions):
    pos = positions.split(",")[0].strip()
    if pos in attack_pos: return "Ataque"
    if pos in mid_pos: return "Meio"
    if pos in def_pos: return "Defesa"
    if pos in gk_pos: return "Goleiro"
    return "Outros"

df["setor"] = df["positions"].apply(classify_sector)

# saída organizada
out_dir = pathlib.Path("./json_ligas")
out_dir.mkdir(exist_ok=True)

# loop por liga
for liga, fname in top5_leagues.items():
    df_liga = df[df["club_league_id"] == liga].copy()

    # médias por clube
    club_means = (
        df_liga.groupby(["club_name","setor"])
        .agg(overall_mean=("overall_rating","mean"))
        .reset_index()
    )
    club_means_pivot = club_means.pivot_table(
        index="club_name",
        columns="setor",
        values="overall_mean"
    ).fillna(0)

    # monta estrutura JSON
    times = {}
    for club, grupo in df_liga.groupby("club_name"):
        jogadores = {}
        for _, row in grupo.iterrows():
            jogadores[row["name"]] = {
                "overall": int(row["overall_rating"]),
                "potential": int(row["potential"]),
                "altura_cm": int(row["height_cm"]),
                "peso_kg": int(row["weight_kg"]),
                "foto": row["image"],
                "playstyles": row["play_styles"].split(",") if pd.notna(row["play_styles"]) else [],
                "setor": row["setor"]
            }

        medias = {
            "ataque": round(club_means_pivot.loc[club].get("Ataque", 0), 1),
            "meio": round(club_means_pivot.loc[club].get("Meio", 0), 1),
            "defesa": round(club_means_pivot.loc[club].get("Defesa", 0), 1),
            "goleiro": round(club_means_pivot.loc[club].get("Goleiro", 0), 1)
        }

        times[club] = {"medias": medias, "jogadores": jogadores}

    # metadados
    json_final = {
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "hash": hashlib.sha256(str(times).encode()).hexdigest(),
        "liga": liga,
        "times": times
    }

    # salva
    with open(out_dir / f"{fname}_2025.json", "w", encoding="utf-8") as f:
        json.dump(json_final, f, ensure_ascii=False, indent=2)

print("Arquivos gerados em ./json_ligas/")
