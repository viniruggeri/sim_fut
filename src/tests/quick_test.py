#!/usr/bin/env python3
"""
Teste rápido para verificar realismo após ajustes
"""

import sys
from pathlib import Path
import random

# Adicionar src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from core.advanced_sim.data_loader import LeagueDataLoader
from core.advanced_sim.simulation.advanced_match import AdvancedMatchSimulator


def test_realism_quick():
    print("🔥 TESTE RÁPIDO DE REALISMO (PÓS-AJUSTES)")
    print("=" * 60)
    
    # Carregar times
    loader = LeagueDataLoader()
    teams = loader.load_league_for_simulation("premier_league")
    team_names = list(teams.keys())
    
    simulator = AdvancedMatchSimulator()
    
    # Simular 20 partidas
    total_goals = 0
    total_shots = 0
    results = []
    
    print("⚽ SIMULANDO 20 PARTIDAS DE TESTE:")
    print("-" * 60)
    
    for i in range(20):
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
        results.append((match_goals, match_shots))
        
        print(f"{i+1:2d}. {home_team[:15]:<15} {result.home_goals}-{result.away_goals} {away_team[:15]:<15} "
              f"(Chutes: {result.home_shots}+{result.away_shots}={match_shots})")
    
    avg_goals = total_goals / 20
    avg_shots = total_shots / 20
    
    # Contar tipos de resultados
    zero_zero = sum(1 for g, s in results if g == 0)
    one_goal = sum(1 for g, s in results if g == 1)
    two_goals = sum(1 for g, s in results if g == 2)
    three_plus = sum(1 for g, s in results if g >= 3)
    
    print(f"\n📊 ANÁLISE DE REALISMO:")
    print(f"   • Média de gols por jogo: {avg_goals:.2f}")
    print(f"   • Média de chutes por jogo: {avg_shots:.1f}")
    print(f"   • Empates 0-0: {zero_zero}/20 ({zero_zero/20*100:.1f}%)")
    print(f"   • Jogos com 1 gol: {one_goal}/20 ({one_goal/20*100:.1f}%)")
    print(f"   • Jogos com 2 gols: {two_goals}/20 ({two_goals/20*100:.1f}%)")
    print(f"   • Jogos com 3+ gols: {three_plus}/20 ({three_plus/20*100:.1f}%)")
    
    print(f"\n🎯 AVALIAÇÃO:")
    if 1.8 <= avg_goals <= 3.2:
        print(f"   ✅ Média de gols REALÍSTICA! (Premier League: ~2.8)")
    else:
        print(f"   ❌ Média de gols {'muito alta' if avg_goals > 3.2 else 'muito baixa'}")
    
    if 16 <= avg_shots <= 28:
        print(f"   ✅ Média de chutes REALÍSTICA! (Premier League: ~22)")
    else:
        print(f"   ❌ Média de chutes {'muito alta' if avg_shots > 28 else 'muito baixa'}")
        
    if zero_zero >= 2:  # Pelo menos 10% de 0-0
        print(f"   ✅ Empates sem gols REALÍSTICOS! (Premier League: ~8-12%)")
    else:
        print(f"   ⚠️  Poucos empates 0-0 (esperado: ~10%)")


if __name__ == "__main__":
    test_realism_quick()