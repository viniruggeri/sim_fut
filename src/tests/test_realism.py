#!/usr/bin/env python3
"""
Teste rápido da temporada com ajustes de realismo
"""

import sys
from pathlib import Path
import random

# Adicionar src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from core.advanced_sim.data_loader import LeagueDataLoader
from core.advanced_sim.simulation.advanced_match import AdvancedMatchSimulator


def test_quick_matches():
    """Testa algumas partidas para ver se os resultados estão realistas"""
    
    print("🔥 TESTE RÁPIDO DE REALISMO")
    print("=" * 50)
    
    # Carregar times
    loader = LeagueDataLoader()
    teams = loader.load_league_for_simulation("premier_league")
    team_names = list(teams.keys())
    
    simulator = AdvancedMatchSimulator()
    
    # Simular 10 partidas aleatórias
    total_goals = 0
    total_shots = 0
    
    print("⚽ SIMULANDO 10 PARTIDAS DE TESTE:")
    print("-" * 50)
    
    for i in range(10):
        home_team = random.choice(team_names)
        away_team = random.choice([t for t in team_names if t != home_team])
        
        result = simulator.simulate_match(
            home_lineup=teams[home_team],
            away_lineup=teams[away_team],
            home_team_name=home_team,
            away_team_name=away_team
        )
        
        match_goals = result.home_goals + result.away_goals
        match_shots = result.home_shots + result.away_shots
        
        total_goals += match_goals
        total_shots += match_shots
        
        print(f"{i+1:2d}. {home_team[:15]:<15} {result.home_goals}-{result.away_goals} {away_team[:15]:<15} "
              f"(Chutes: {result.home_shots}+{result.away_shots}={match_shots})")
    
    avg_goals = total_goals / 10
    avg_shots = total_shots / 10
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Média de gols por jogo: {avg_goals:.1f}")
    print(f"   • Média de chutes por jogo: {avg_shots:.1f}")
    
    # Análise de realismo
    if 2.0 <= avg_goals <= 3.5:
        print(f"   ✅ Média de gols realística! (Premier League: ~2.8)")
    else:
        print(f"   ❌ Média de gols {'muito alta' if avg_goals > 3.5 else 'muito baixa'}")
    
    if 20 <= avg_shots <= 30:
        print(f"   ✅ Média de chutes realística! (Premier League: ~25)")
    else:
        print(f"   ❌ Média de chutes {'muito alta' if avg_shots > 30 else 'muito baixa'}")


if __name__ == "__main__":
    test_quick_matches()