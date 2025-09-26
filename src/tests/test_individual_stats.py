#!/usr/bin/env python3
"""
Sistema para tracking das estatísticas individuais dos jogadores
"""

import sys
from pathlib import Path
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass, field

# Adicionar src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from core.advanced_sim.data_loader import LeagueDataLoader
from core.advanced_sim.simulation.advanced_match import AdvancedMatchSimulator, TeamLineup


@dataclass
class PlayerSeasonStats:
    """Estatísticas de um jogador durante a temporada"""
    player_name: str
    team_name: str
    position: str
    overall: int
    
    # Estatísticas de jogo
    matches_played: int = 0
    minutes_played: int = 0
    goals: int = 0
    assists: int = 0
    shots: int = 0
    shots_on_target: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    
    # Médias calculadas
    @property
    def goals_per_game(self) -> float:
        return self.goals / max(1, self.matches_played)
    
    @property
    def assists_per_game(self) -> float:
        return self.assists / max(1, self.matches_played)


class PlayerStatsTracker:
    """Sistema de tracking das estatísticas dos jogadores"""
    
    def __init__(self, teams: Dict[str, TeamLineup]):
        self.teams = teams
        self.player_stats: Dict[str, PlayerSeasonStats] = {}
        
        # Inicializar estatísticas para todos os jogadores
        for team_name, lineup in teams.items():
            for player in lineup.players + lineup.substitutes:
                self.player_stats[player.id] = PlayerSeasonStats(
                    player_name=player.name,
                    team_name=team_name,
                    position=player.position.value,
                    overall=player.current_overall
                )
    
    def update_match_stats(self, match_result, home_team: str, away_team: str):
        """Atualiza estatísticas após uma partida"""
        
        # Atualizar estatísticas do time da casa
        for player_id, performance in match_result.home_performances.items():
            if player_id in self.player_stats:
                stats = self.player_stats[player_id]
                stats.matches_played += 1
                stats.minutes_played += performance.minutes_played
                stats.goals += performance.goals
                stats.assists += performance.assists
                stats.shots += performance.shots
                stats.shots_on_target += performance.shots_on_target
                stats.yellow_cards += performance.yellow_cards
                stats.red_cards += performance.red_cards
        
        # Atualizar estatísticas do time visitante
        for player_id, performance in match_result.away_performances.items():
            if player_id in self.player_stats:
                stats = self.player_stats[player_id]
                stats.matches_played += 1
                stats.minutes_played += performance.minutes_played
                stats.goals += performance.goals
                stats.assists += performance.assists
                stats.shots += performance.shots
                stats.shots_on_target += performance.shots_on_target
                stats.yellow_cards += performance.yellow_cards
                stats.red_cards += performance.red_cards
    
    def get_top_scorers(self, limit: int = 10) -> List[PlayerSeasonStats]:
        """Retorna os artilheiros da temporada"""
        return sorted(
            [stats for stats in self.player_stats.values() if stats.goals > 0],
            key=lambda x: (x.goals, x.assists),
            reverse=True
        )[:limit]
    
    def get_top_assisters(self, limit: int = 10) -> List[PlayerSeasonStats]:
        """Retorna os maiores assistentes da temporada"""
        return sorted(
            [stats for stats in self.player_stats.values() if stats.assists > 0],
            key=lambda x: (x.assists, x.goals),
            reverse=True
        )[:limit]
    
    def get_team_stats(self, team_name: str) -> List[PlayerSeasonStats]:
        """Retorna estatísticas de todos os jogadores de um time"""
        return [stats for stats in self.player_stats.values() 
                if stats.team_name == team_name and stats.matches_played > 0]
    
    def print_top_scorers(self):
        """Imprime tabela dos artilheiros"""
        print(f"\n{'='*80}")
        print(f"⚽ TOP 10 ARTILHEIROS DA TEMPORADA")
        print(f"{'='*80}")
        print(f"{'Pos':<3} {'Jogador':<20} {'Time':<18} {'Gols':<5} {'Assist':<6} {'Jogos':<5} {'Média':<5}")
        print(f"{'-'*80}")
        
        for i, stats in enumerate(self.get_top_scorers(), 1):
            print(f"{i:<3} {stats.player_name[:19]:<20} {stats.team_name[:17]:<18} "
                  f"{stats.goals:<5} {stats.assists:<6} {stats.matches_played:<5} "
                  f"{stats.goals_per_game:.2f}")
    
    def print_top_assisters(self):
        """Imprime tabela dos maiores assistentes"""
        print(f"\n{'='*80}")
        print(f"🎯 TOP 10 ASSISTÊNCIAS DA TEMPORADA")
        print(f"{'='*80}")
        print(f"{'Pos':<3} {'Jogador':<20} {'Time':<18} {'Assist':<6} {'Gols':<5} {'Jogos':<5} {'Média':<5}")
        print(f"{'-'*80}")
        
        for i, stats in enumerate(self.get_top_assisters(), 1):
            print(f"{i:<3} {stats.player_name[:19]:<20} {stats.team_name[:17]:<18} "
                  f"{stats.assists:<6} {stats.goals:<5} {stats.matches_played:<5} "
                  f"{stats.assists_per_game:.2f}")
    
    def print_team_detailed_stats(self, team_name: str):
        """Imprime estatísticas detalhadas de um time"""
        team_players = self.get_team_stats(team_name)
        if not team_players:
            print(f"❌ Nenhuma estatística encontrada para {team_name}")
            return
        
        # Ordenar por gols + assistências
        team_players.sort(key=lambda x: (x.goals + x.assists, x.overall), reverse=True)
        
        print(f"\n{'='*90}")
        print(f"📊 ESTATÍSTICAS DETALHADAS - {team_name.upper()}")
        print(f"{'='*90}")
        print(f"{'Jogador':<20} {'Pos':<4} {'OVR':<3} {'J':<2} {'G':<2} {'A':<2} {'FC':<3} {'CA':<2} {'G/J':<4}")
        print(f"{'-'*90}")
        
        for stats in team_players:
            print(f"{stats.player_name[:19]:<20} {stats.position[:3]:<4} "
                  f"{stats.overall:<3} {stats.matches_played:<2} {stats.goals:<2} "
                  f"{stats.assists:<2} {stats.shots:<3} {stats.yellow_cards:<2} "
                  f"{stats.goals_per_game:.2f}")


def test_individual_stats():
    """Testa o sistema de estatísticas individuais"""
    
    print("📊 TESTE DE ESTATÍSTICAS INDIVIDUAIS")
    print("=" * 60)
    
    # Carregar times
    loader = LeagueDataLoader()
    teams = loader.load_league_for_simulation("premier_league")
    
    # Criar tracker de estatísticas
    stats_tracker = PlayerStatsTracker(teams)
    simulator = AdvancedMatchSimulator()
    
    # Simular algumas partidas
    team_names = list(teams.keys())
    print(f"⚽ Simulando 20 partidas para coletar dados...")
    
    for i in range(20):
        home_team = random.choice(team_names)
        away_team = random.choice([t for t in team_names if t != home_team])
        
        result = simulator.simulate_match(
            home_lineup=teams[home_team],
            away_lineup=teams[away_team],
            home_team_name=home_team,
            away_team_name=away_team
        )
        
        # Atualizar estatísticas
        stats_tracker.update_match_stats(result, home_team, away_team)
        
        if i % 5 == 0:
            print(f"   Partida {i+1}: {home_team} {result.home_goals}-{result.away_goals} {away_team}")
    
    # Mostrar estatísticas
    stats_tracker.print_top_scorers()
    stats_tracker.print_top_assisters()
    
    # Mostrar estatísticas de um time específico
    sample_team = random.choice(team_names)
    stats_tracker.print_team_detailed_stats(sample_team)
    
    print(f"\n✅ Sistema de estatísticas individuais funcionando!")


if __name__ == "__main__":
    test_individual_stats()