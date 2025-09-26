from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import date, datetime, timedelta
from enum import Enum
import random

from .advanced_match import AdvancedMatchResult, AdvancedMatchSimulator, TeamLineup
from ..models.player import AdvancedPlayer


class MatchweekStatus(Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    POSTPONED = "Postponed"


@dataclass
class SeasonFixture:
    matchweek: int
    home_team: str
    away_team: str
    scheduled_date: date
    kickoff_time: str = "15:00"
    
    # Resultado (preenchido após o jogo)
    result: Optional[AdvancedMatchResult] = None
    status: MatchweekStatus = MatchweekStatus.SCHEDULED
    
    attendance: int = 0
    weather: str = "Clear"
    temperature: int = 20  # Celsius


@dataclass
class SeasonCalendar:
    season_year: str  # e.g., "2024-25"
    teams: List[str]
    fixtures: List[SeasonFixture] = field(default_factory=list)
    
    # Configurações da temporada
    start_date: date = field(default_factory=lambda: date(2024, 8, 17))  # Típico início da Premier League
    winter_break_start: Optional[date] = None
    winter_break_end: Optional[date] = None
    
    # Estatísticas da temporada
    current_matchweek: int = 1
    completed_matchweeks: int = 0
    
    def generate_fixtures(self):
        """Gera calendário completo da temporada (turno e returno)"""
        if len(self.teams) < 2:
            raise ValueError("Precisa de pelo menos 2 times para gerar calendário")
        
        num_teams = len(self.teams)
        if num_teams % 2 != 0:
            raise ValueError("Número de times deve ser par")
        
        # Algoritmo round-robin para gerar todos os confrontos
        fixtures_first_round = []
        fixtures_second_round = []
        
        # Primeira volta
        for round_num in range(num_teams - 1):
            round_fixtures = []
            
            for match_num in range(num_teams // 2):
                home_idx = match_num
                away_idx = num_teams - 1 - match_num
                
                if round_num % 2 == 0:
                    home_team = self.teams[home_idx]
                    away_team = self.teams[away_idx]
                else:
                    home_team = self.teams[away_idx]
                    away_team = self.teams[home_idx]
                
                round_fixtures.append((home_team, away_team))
            
            fixtures_first_round.append(round_fixtures)
            
            # Rotacionar times (exceto o primeiro)
            self.teams = [self.teams[0]] + [self.teams[-1]] + self.teams[1:-1]
        
        # Segunda volta (inverter mando de campo)
        for round_fixtures in fixtures_first_round:
            second_round = [(away, home) for home, away in round_fixtures]
            fixtures_second_round.append(second_round)
        
        # Converter para SeasonFixture com datas
        current_date = self.start_date
        matchweek = 1
        
        # Primeira volta
        for round_fixtures in fixtures_first_round:
            for home_team, away_team in round_fixtures:
                fixture = SeasonFixture(
                    matchweek=matchweek,
                    home_team=home_team,
                    away_team=away_team,
                    scheduled_date=current_date,
                    attendance=random.randint(30000, 75000)
                )
                self.fixtures.append(fixture)
            
            matchweek += 1
            current_date += timedelta(days=7)  # Jogos semanais
            
            # Pausa para datas FIFA (algumas rodadas)
            if matchweek % 4 == 0:
                current_date += timedelta(days=7)
        
        # Segunda volta
        for round_fixtures in fixtures_second_round:
            for home_team, away_team in round_fixtures:
                fixture = SeasonFixture(
                    matchweek=matchweek,
                    home_team=home_team,
                    away_team=away_team,
                    scheduled_date=current_date,
                    attendance=random.randint(30000, 75000)
                )
                self.fixtures.append(fixture)
            
            matchweek += 1
            current_date += timedelta(days=7)
            
            # Pausa de inverno
            if self.winter_break_start and current_date >= self.winter_break_start:
                current_date = self.winter_break_end or current_date + timedelta(days=14)
    
    def get_matchweek_fixtures(self, matchweek: int) -> List[SeasonFixture]:
        """Retorna jogos de uma rodada específica"""
        return [f for f in self.fixtures if f.matchweek == matchweek]
    
    def get_team_fixtures(self, team_name: str, completed_only: bool = False) -> List[SeasonFixture]:
        """Retorna jogos de um time específico"""
        team_fixtures = [f for f in self.fixtures if f.home_team == team_name or f.away_team == team_name]
        
        if completed_only:
            team_fixtures = [f for f in team_fixtures if f.status == MatchweekStatus.COMPLETED]
        
        return team_fixtures
    
    def get_next_fixtures(self, team_name: str, count: int = 5) -> List[SeasonFixture]:
        """Retorna próximos jogos de um time"""
        upcoming = [f for f in self.fixtures 
                   if (f.home_team == team_name or f.away_team == team_name) 
                   and f.status == MatchweekStatus.SCHEDULED]
        
        return upcoming[:count]
    
    def is_matchweek_complete(self, matchweek: int) -> bool:
        """Verifica se uma rodada foi completamente disputada"""
        matchweek_fixtures = self.get_matchweek_fixtures(matchweek)
        return all(f.status == MatchweekStatus.COMPLETED for f in matchweek_fixtures)


@dataclass 
class LeagueTable:
    """Tabela de classificação da liga"""
    teams: Dict[str, Dict[str, int]] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.teams:
            self.teams = {}
    
    def initialize_teams(self, team_names: List[str]):
        """Inicializa tabela com times zerados"""
        for team in team_names:
            self.teams[team] = {
                "matches_played": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0,
                "goal_difference": 0,
                "points": 0
            }
    
    def update_from_result(self, result: AdvancedMatchResult):
        """Atualiza tabela com resultado de uma partida"""
        home_team = result.home_team
        away_team = result.away_team
        home_goals = result.home_goals
        away_goals = result.away_goals
        
        # Atualizar estatísticas básicas
        self.teams[home_team]["matches_played"] += 1
        self.teams[away_team]["matches_played"] += 1
        
        self.teams[home_team]["goals_for"] += home_goals
        self.teams[home_team]["goals_against"] += away_goals
        self.teams[away_team]["goals_for"] += away_goals
        self.teams[away_team]["goals_against"] += home_goals
        
        # Determinar resultado
        if home_goals > away_goals:
            # Vitória do time da casa
            self.teams[home_team]["wins"] += 1
            self.teams[home_team]["points"] += 3
            self.teams[away_team]["losses"] += 1
            
        elif away_goals > home_goals:
            # Vitória do time visitante
            self.teams[away_team]["wins"] += 1
            self.teams[away_team]["points"] += 3
            self.teams[home_team]["losses"] += 1
            
        else:
            # Empate
            self.teams[home_team]["draws"] += 1
            self.teams[home_team]["points"] += 1
            self.teams[away_team]["draws"] += 1
            self.teams[away_team]["points"] += 1
        
        # Atualizar saldo de gols
        self.teams[home_team]["goal_difference"] = (
            self.teams[home_team]["goals_for"] - self.teams[home_team]["goals_against"]
        )
        self.teams[away_team]["goal_difference"] = (
            self.teams[away_team]["goals_for"] - self.teams[away_team]["goals_against"]
        )
    
    def get_sorted_table(self) -> List[Tuple[str, Dict[str, int]]]:
        """Retorna tabela ordenada por pontos, saldo de gols, etc."""
        return sorted(
            self.teams.items(),
            key=lambda x: (
                x[1]["points"],           # Pontos (maior primeiro)
                x[1]["goal_difference"],  # Saldo de gols
                x[1]["goals_for"],        # Gols marcados
                -x[1]["goals_against"]    # Gols sofridos (menor primeiro)
            ),
            reverse=True
        )
    
    def get_team_position(self, team_name: str) -> int:
        """Retorna posição atual do time na tabela"""
        sorted_table = self.get_sorted_table()
        for i, (team, stats) in enumerate(sorted_table):
            if team == team_name:
                return i + 1
        return len(sorted_table)


class SeasonSimulator:
    """Simulador completo de temporada"""
    
    def __init__(self):
        self.calendar: Optional[SeasonCalendar] = None
        self.table: Optional[LeagueTable] = None
        self.match_simulator = AdvancedMatchSimulator()
        
        # Dados dos times (seriam carregados de um arquivo)
        self.team_lineups: Dict[str, TeamLineup] = {}
        self.player_stats: Dict[str, Dict] = {}  # Estatísticas acumuladas dos jogadores
    
    def initialize_season(
        self, 
        team_names: List[str], 
        season_year: str = "2024-25",
        start_date: Optional[date] = None
    ):
        """Inicializa uma nova temporada"""
        if start_date is None:
            start_date = date(2024, 8, 17)
        
        self.calendar = SeasonCalendar(
            season_year=season_year,
            teams=team_names.copy(),  # Importante fazer cópia
            start_date=start_date
        )
        
        self.table = LeagueTable()
        self.table.initialize_teams(team_names)
        
        # Gerar calendário completo
        self.calendar.generate_fixtures()
        
        print(f"Temporada {season_year} inicializada com {len(team_names)} times")
        print(f"Total de jogos: {len(self.calendar.fixtures)}")
    
    def simulate_matchweek(self, matchweek: int) -> List[AdvancedMatchResult]:
        """Simula uma rodada completa"""
        if not self.calendar or not self.table:
            raise ValueError("Temporada não foi inicializada")
        
        fixtures = self.calendar.get_matchweek_fixtures(matchweek)
        results = []
        
        print(f"\n=== RODADA {matchweek} ===")
        
        for fixture in fixtures:
            # Aqui você carregaria os lineups reais dos times
            # Por enquanto, vamos usar lineups mockados
            home_lineup = self.team_lineups.get(fixture.home_team)
            away_lineup = self.team_lineups.get(fixture.away_team)
            
            if not home_lineup or not away_lineup:
                print(f"Lineups não encontrados para {fixture.home_team} vs {fixture.away_team}")
                continue
            
            # Simular partida
            result = self.match_simulator.simulate_match(
                home_lineup=home_lineup,
                away_lineup=away_lineup,
                home_team_name=fixture.home_team,
                away_team_name=fixture.away_team,
                match_date=fixture.scheduled_date
            )
            
            # Atualizar fixture
            fixture.result = result
            fixture.status = MatchweekStatus.COMPLETED
            fixture.attendance = random.randint(30000, 75000)
            
            # Atualizar tabela
            self.table.update_from_result(result)
            
            results.append(result)
            
            # Mostrar resultado
            print(f"{result.home_team} {result.home_goals}-{result.away_goals} {result.away_team}")
            
            # Mostrar eventos principais (gols)
            goals = [e for e in result.events if e.event_type.value == "Goal"]
            for goal in goals:
                print(f"  {goal.minute}' {goal.description}")
        
        # Atualizar rodada atual
        if self.calendar.is_matchweek_complete(matchweek):
            self.calendar.completed_matchweeks += 1
            self.calendar.current_matchweek = matchweek + 1
        
        return results
    
    def simulate_full_season(self) -> Dict:
        """Simula temporada completa"""
        if not self.calendar:
            raise ValueError("Temporada não foi inicializada")
        
        total_matchweeks = len(self.calendar.teams) * 2 - 2  # Turno e returno
        
        print(f"Simulando temporada completa: {total_matchweeks} rodadas")
        
        season_results = []
        
        for matchweek in range(1, total_matchweeks + 1):
            matchweek_results = self.simulate_matchweek(matchweek)
            season_results.extend(matchweek_results)
            
            # Mostrar tabela a cada 5 rodadas
            if matchweek % 5 == 0:
                self.print_table()
        
        # Tabela final
        print("\n" + "="*50)
        print("CLASSIFICAÇÃO FINAL")
        print("="*50)
        self.print_table()
        
        return {
            "season_year": self.calendar.season_year,
            "total_matches": len(season_results),
            "final_table": self.table.get_sorted_table() if self.table else [],
            "champion": self.table.get_sorted_table()[0][0] if self.table and self.table.teams else "Unknown"
        }
    
    def print_table(self):
        """Imprime tabela atual"""
        if not self.table:
            return
        
        sorted_table = self.table.get_sorted_table()
        
        print(f"\n{'Pos':<3} {'Time':<25} {'J':<3} {'V':<3} {'E':<3} {'D':<3} {'GP':<3} {'GC':<3} {'SG':<4} {'Pts':<3}")
        print("-" * 70)
        
        for i, (team, stats) in enumerate(sorted_table):
            print(f"{i+1:<3} {team:<25} {stats['matches_played']:<3} {stats['wins']:<3} "
                  f"{stats['draws']:<3} {stats['losses']:<3} {stats['goals_for']:<3} "
                  f"{stats['goals_against']:<3} {stats['goal_difference']:<4} {stats['points']:<3}")
    
    def get_player_season_stats(self, player_id: str) -> Dict:
        """Retorna estatísticas acumuladas de um jogador na temporada"""
        return self.player_stats.get(player_id, {})