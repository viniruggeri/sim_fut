#!/usr/bin/env python3
"""
Simulador de Temporada Completa - Sistema Plug and Play
Simula uma temporada inteira usando dados reais dos times
"""

import sys
from pathlib import Path
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json
import pandas as pd
import hashlib

# Adicionar src ao path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from core.advanced_sim.data_loader import LeagueDataLoader
from core.advanced_sim.simulation.advanced_match import AdvancedMatchSimulator, TeamLineup
from core.advanced_sim.simulation.season import SeasonSimulator

# Adicionar sistema de estatísticas dos jogadores
sys.path.insert(0, str(Path(__file__).parent.parent))
from tests.test_individual_stats import PlayerStatsTracker


class LeagueTable:
    """Tabela da liga com pontuação e estatísticas"""
    
    def __init__(self, teams: List[str]):
        self.teams = {team: {
            'points': 0,
            'matches': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_for': 0,
            'goals_against': 0,
            'goal_difference': 0
        } for team in teams}
    
    def add_match_result(self, home_team: str, away_team: str, home_goals: int, away_goals: int):
        """Adiciona resultado de uma partida à tabela"""
        
        # Atualizar estatísticas do time da casa
        self.teams[home_team]['matches'] += 1
        self.teams[home_team]['goals_for'] += home_goals
        self.teams[home_team]['goals_against'] += away_goals
        
        # Atualizar estatísticas do time visitante
        self.teams[away_team]['matches'] += 1
        self.teams[away_team]['goals_for'] += away_goals
        self.teams[away_team]['goals_against'] += home_goals
        
        # Determinar resultado
        if home_goals > away_goals:  # Vitória da casa
            self.teams[home_team]['wins'] += 1
            self.teams[home_team]['points'] += 3
            self.teams[away_team]['losses'] += 1
            
        elif away_goals > home_goals:  # Vitória visitante
            self.teams[away_team]['wins'] += 1
            self.teams[away_team]['points'] += 3
            self.teams[home_team]['losses'] += 1
            
        else:  # Empate
            self.teams[home_team]['draws'] += 1
            self.teams[home_team]['points'] += 1
            self.teams[away_team]['draws'] += 1
            self.teams[away_team]['points'] += 1
        
        # Calcular saldo de gols
        for team in [home_team, away_team]:
            self.teams[team]['goal_difference'] = (
                self.teams[team]['goals_for'] - self.teams[team]['goals_against']
            )
    
    def get_table(self) -> List[Tuple[str, Dict]]:
        """Retorna tabela ordenada por pontuação"""
        return sorted(
            self.teams.items(),
            key=lambda x: (x[1]['points'], x[1]['goal_difference'], x[1]['goals_for']),
            reverse=True
        )
    
    def print_table(self, title: str = "TABELA DA LIGA"):
        """Imprime a tabela formatada"""
        print(f"\n{'='*80}")
        print(f"[CAMPEAO] {title}")
        print(f"{'='*80}")
        print(f"{'Pos':<3} {'Time':<20} {'J':<3} {'V':<3} {'E':<3} {'D':<3} {'GP':<4} {'GC':<4} {'SG':<4} {'Pts':<4}")
        print(f"{'-'*80}")
        
        for pos, (team, stats) in enumerate(self.get_table(), 1):
            # Ícones para posições especiais
            icon = ""
            if pos == 1:
                icon = "[1st]"
            elif pos <= 4:
                icon = "[CL]"  # Champions League
            elif pos <= 6:
                icon = "[EL]"  # Europa League
            elif pos >= len(self.teams) - 2:
                icon = "[REL]"  # Rebaixamento
            
            print(f"{pos:<3} {team:<18} {icon} {stats['matches']:<3} {stats['wins']:<3} "
                  f"{stats['draws']:<3} {stats['losses']:<3} {stats['goals_for']:<4} "
                  f"{stats['goals_against']:<4} {stats['goal_difference']:+4} {stats['points']:<4}")


class FullSeasonSimulator:
    """Simulador de temporada completa"""
    
    def __init__(self, league_name: str = "premier_league"):
        self.league_name = league_name
        self.loader = LeagueDataLoader()
        self.simulator = AdvancedMatchSimulator()
        
        # Carregar times da liga
        print(f"[LOADING] Carregando {league_name.replace('_', ' ').title()}...")
        self.teams = self.loader.load_league_for_simulation(league_name)
        self.team_names = list(self.teams.keys())
        
        # Criar tabela da liga
        self.table = LeagueTable(self.team_names)
        
        # Criar tracker de estatísticas dos jogadores
        self.player_stats = PlayerStatsTracker(self.teams)
        
        # Configurações para exportação
        self.output_dir = Path(__file__).parent.parent / "data" / "processed" / "resultados" / league_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[OK] {len(self.team_names)} times carregados!")
        
    def generate_fixtures(self) -> List[Tuple[str, str]]:
        """Gera todos os confrontos do campeonato (ida e volta)"""
        fixtures = []
        
        # Cada time joga contra cada outro 2 vezes (casa e fora)
        for i, home_team in enumerate(self.team_names):
            for j, away_team in enumerate(self.team_names):
                if i != j:
                    fixtures.append((home_team, away_team))
        
        # Embaralhar a ordem dos jogos
        random.shuffle(fixtures)
        
        return fixtures
    
    def simulate_match(self, home_team: str, away_team: str) -> Tuple[int, int]:
        """Simula uma partida entre dois times"""
        home_lineup = self.teams[home_team]
        away_lineup = self.teams[away_team]
        
        match_result = self.simulator.simulate_match(
            home_lineup=home_lineup,
            away_lineup=away_lineup,
            home_team_name=home_team,
            away_team_name=away_team
        )
        
        # Atualizar estatísticas dos jogadores
        self.player_stats.update_match_stats(match_result, home_team, away_team)
        
        return match_result.home_goals, match_result.away_goals
    
    def simulate_full_season(self, show_results: bool = False) -> LeagueTable:
        """Simula uma temporada completa"""
        
        print(f"\n[SIMULACAO] INICIANDO SIMULAÇÃO DA TEMPORADA {self.league_name.replace('_', ' ').upper()}")
        print(f"[INFO] Total de partidas: {len(self.team_names) * (len(self.team_names) - 1)}")
        
        fixtures = self.generate_fixtures()
        completed_matches = 0
        
        # Simular todas as partidas
        for home_team, away_team in fixtures:
            home_goals, away_goals = self.simulate_match(home_team, away_team)
            
            # Adicionar resultado à tabela
            self.table.add_match_result(home_team, away_team, home_goals, away_goals)
            completed_matches += 1
            
            # Mostrar progresso
            if completed_matches % 50 == 0:
                progress = (completed_matches / len(fixtures)) * 100
                print(f"[PROGRESS] Progresso: {progress:.1f}% ({completed_matches}/{len(fixtures)} jogos)")
            
            # Mostrar resultado se solicitado
            if show_results and completed_matches <= 10:  # Primeiros 10 jogos
                result_symbol = "[WIN]" if home_goals != away_goals else "[DRAW]"
                print(f"   {result_symbol} {home_team} {home_goals}-{away_goals} {away_team}")
        
        print(f"[OK] Temporada concluída! {completed_matches} partidas simuladas.")
        
        return self.table
    
    def export_results(self):
        """Exporta resultados em JSON e CSV igual ao simulador simples"""
        
        # Criar timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        league_clean = self.league_name.replace("_", " ").title()
        
        # 1. Exportar tabela da liga
        table_data = self.table.get_table()
        
        # Converter para DataFrame
        df_table = pd.DataFrame([
            {
                'Time': team,
                'J': stats['matches'], 
                'V': stats['wins'],
                'E': stats['draws'],
                'D': stats['losses'],
                'GP': stats['goals_for'],
                'GC': stats['goals_against'], 
                'SG': stats['goal_difference'],
                'P': stats['points']
            }
            for team, stats in table_data
        ])
        
        # 2. Exportar estatísticas dos jogadores
        all_players = []
        for player_id, stats in self.player_stats.player_stats.items():
            if stats.matches_played > 0:  # Só jogadores que jogaram
                all_players.append({
                    'Nome': stats.player_name,
                    'Time': stats.team_name,
                    'Posicao': stats.position,
                    'Overall': int(stats.overall),
                    'Jogos': int(stats.matches_played),
                    'Minutos': int(stats.minutes_played),
                    'Gols': int(stats.goals),
                    'Assistencias': int(stats.assists),
                    'Finalizacoes': int(stats.shots),
                    'Chutes_Alvo': int(stats.shots_on_target),
                    'Cartoes_Amarelos': int(stats.yellow_cards),
                    'Cartoes_Vermelhos': int(stats.red_cards),
                    'Media_Gols': round(float(stats.goals_per_game), 3),
                    'Media_Assists': round(float(stats.assists_per_game), 3)
                })
        
        df_players = pd.DataFrame(all_players)
        df_players = df_players.sort_values(['Gols', 'Assistencias'], ascending=[False, False])
        
        # 3. Gerar hash SHA256
        combined_data = df_table.to_json() + df_players.to_json()
        hash_value = hashlib.sha256(combined_data.encode()).hexdigest()
        
        # 4. Criar estrutura JSON completa
        output_data = {
            "version": "2.0.0",
            "simulation_type": "advanced",
            "created_at": datetime.now().isoformat(),
            "league": league_clean,
            "hash": f"sha256:{hash_value}",
            "summary": {
                "total_matches": int(len(self.team_names) * (len(self.team_names) - 1)),
                "total_goals": int(sum(team[1]['goals_for'] for team in table_data)),
                "total_players": int(len([p for p in all_players if p['Jogos'] > 0])),
                "champion": str(table_data[0][0]),
                "top_scorer": str(df_players.iloc[0]['Nome']) if not df_players.empty else None,
                "top_scorer_goals": int(df_players.iloc[0]['Gols']) if not df_players.empty else 0
            },
            "tabela_final": df_table.to_dict(orient="records"),
            "estatisticas_jogadores": df_players.to_dict(orient="records"),
            "top_10_artilheiros": df_players.head(10).to_dict(orient="records"),
            "top_10_assistencias": df_players.sort_values(['Assistencias', 'Gols'], ascending=[False, False]).head(10).to_dict(orient="records")
        }
        
        # 5. Salvar arquivos
        base_filename = f"resultados_{self.league_name}_{timestamp}"
        
        # CSV da tabela
        csv_table_path = self.output_dir / f"{base_filename}_tabela.csv"
        df_table.to_csv(csv_table_path, sep=";", index=False, encoding="utf-8")
        
        # CSV dos jogadores
        csv_players_path = self.output_dir / f"{base_filename}_jogadores.csv" 
        df_players.to_csv(csv_players_path, sep=";", index=False, encoding="utf-8")
        
        # JSON completo
        json_path = self.output_dir / f"{base_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 DADOS EXPORTADOS:")
        print(f"   [TABELA] Tabela: {csv_table_path}")
        print(f"   👥 Jogadores: {csv_players_path}")
        print(f"   📋 Completo: {json_path}")
        print(f"   🔐 Hash: {hash_value[:16]}...")
        
        return {
            'table_csv': csv_table_path,
            'players_csv': csv_players_path, 
            'json': json_path,
            'hash': hash_value
        }
    
    def show_final_results(self):
        """Mostra resultados finais da temporada"""
        
        # Tabela final
        self.table.print_table(f"RESULTADO FINAL - {self.league_name.replace('_', ' ').upper()} 2025")
        
        # Estatísticas interessantes
        table_data = self.table.get_table()
        
        print(f"\n[DESTAQUES] DESTAQUES DA TEMPORADA:")
        
        # Campeão
        champion = table_data[0]
        print(f"[CAMPEAO] CAMPEÃO: {champion[0]} com {champion[1]['points']} pontos")
        
        # Vice-campeão
        runner_up = table_data[1]
        print(f"[2nd] Vice-campeão: {runner_up[0]} com {runner_up[1]['points']} pontos")
        
        # Rebaixados
        relegated = table_data[-3:]
        relegated.reverse()  # Mostrar do pior pro melhor
        print(f"\n🔴 REBAIXAMENTO:")
        for pos, (team, stats) in enumerate(relegated, len(table_data)-2):
            print(f"   {pos}º {team} - {stats['points']} pts")
        
        # Top scorers e assistências
        print(f"\n[ARTILHEIROS] TOP 10 ARTILHEIROS:")
        self.player_stats.print_top_scorers()
        
        print(f"\n🎯 TOP 10 ASSISTÊNCIAS:")
        self.player_stats.print_top_assisters()
        
        # Exportar dados
        print(f"\n📂 EXPORTANDO RESULTADOS...")
        export_info = self.export_results()
        
        return export_info
        
        # Artilharia (maior número de gols marcados)
        best_attack = max(table_data, key=lambda x: x[1]['goals_for'])
        print(f"\n[ATAQUE] MELHOR ATAQUE: {best_attack[0]} ({best_attack[1]['goals_for']} gols)")
        
        # Melhor defesa
        best_defense = min(table_data, key=lambda x: x[1]['goals_against'])
        print(f"🛡️  MELHOR DEFESA: {best_defense[0]} ({best_defense[1]['goals_against']} gols sofridos)")
        
        # Classificação para competições europeias
        print(f"\n🌍 COMPETIÇÕES EUROPEIAS 2026:")
        print(f"   🔵 Champions League: {', '.join([team[0] for team in table_data[:4]])}")
        if len(table_data) > 4:
            print(f"   🟡 Europa League: {', '.join([team[0] for team in table_data[4:6]])}")
        
        # Mostrar estatísticas individuais dos jogadores
        print(f"\n" + "="*80)
        print(f"👥 ESTATÍSTICAS INDIVIDUAIS DA TEMPORADA")
        print(f"="*80)
        
        # Top artilheiros
        self.player_stats.print_top_scorers()
        
        # Top assistentes  
        self.player_stats.print_top_assisters()


def main():
    """Função principal - simula uma temporada completa"""
    import argparse
    import os
    
    # Parser de argumentos
    parser = argparse.ArgumentParser(description='Simulador de Temporada Completa')
    parser.add_argument('--league', 
                       type=str, 
                       default=None,
                       help='Liga para simular (premier_league, bundesliga, la_liga, serie_a, ligue_1)')
    
    args = parser.parse_args()
    
    print("="*80)
    print("[*] SIMULADOR DE TEMPORADA COMPLETA - SISTEMA PLUG & PLAY")
    print("="*80)
    
    # Definir seed para reproduzibilidade (opcional)
    random.seed(42)
    
    # Mostrar ligas disponíveis
    loader = LeagueDataLoader()
    available_leagues = loader.get_available_leagues()
    
    print(f"\n[LIST] LIGAS DISPONÍVEIS:")
    for i, league in enumerate(available_leagues, 1):
        print(f"   {i}. {league.replace('_', ' ').title()}")
    
    # Escolher liga (por argumento, variável de ambiente ou padrão)
    if args.league:
        league_choice = args.league
    elif os.getenv('LEAGUE'):
        league_choice = os.getenv('LEAGUE')
    else:
        league_choice = "premier_league"
    
    # Validar se a liga existe
    if league_choice not in available_leagues:
        print(f"[ERROR] Liga '{league_choice}' não encontrada!")
        print(f"Ligas disponíveis: {', '.join(available_leagues)}")
        return
    
    print(f"\n[TARGET] Simulando: {league_choice.replace('_', ' ').title()}")
    
    # Criar simulador
    season_sim = FullSeasonSimulator(league_choice)
    
    # Mostrar times carregados
    print(f"\n[PARTICIPANTES] TIMES PARTICIPANTES:")
    for i, team in enumerate(season_sim.team_names, 1):
        overall = season_sim.teams[team].get_team_rating()
        print(f"   {i:2d}. {team:<20} (Overall: {overall:.1f})")
    
    # Simular temporada
    final_table = season_sim.simulate_full_season(show_results=True)
    
    # Mostrar resultados
    season_sim.show_final_results()
    
    print(f"\n[OK] Simulação da {league_choice.replace('_', ' ').title()} 2025 concluída!")
    print(f"[GAME] Sistema funcionando perfeitamente com dados reais dos jogadores!")


if __name__ == "__main__":
    main()