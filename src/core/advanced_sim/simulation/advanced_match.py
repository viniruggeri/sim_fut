from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, date, timedelta
import random
import numpy as np

from ..models.player import AdvancedPlayer, Position, SeasonStats
from ..stats.tatics.formations import Formation, FormationType, FORMATIONS, calculate_tactical_advantage


class EventType(Enum):
    GOAL = "Goal"
    ASSIST = "Assist"
    YELLOW_CARD = "Yellow Card"
    RED_CARD = "Red Card"
    SUBSTITUTION = "Substitution"
    INJURY = "Injury"
    SAVE = "Save"
    SHOT_ON_TARGET = "Shot on Target"
    SHOT_OFF_TARGET = "Shot off Target"
    TACKLE = "Tackle"
    INTERCEPTION = "Interception"
    KEY_PASS = "Key Pass"


@dataclass
class MatchEvent:
    minute: int
    event_type: EventType
    player_id: str
    team_name: str
    description: str
    assisted_by: Optional[str] = None
    rating_impact: float = 0.0  # Impacto no rating do jogador (-2.0 a +2.0)


@dataclass
class PlayerMatchPerformance:
    player_id: str
    minutes_played: int = 0
    goals: int = 0
    assists: int = 0
    shots: int = 0
    shots_on_target: int = 0
    key_passes: int = 0
    tackles: int = 0
    interceptions: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    saves: int = 0  # Para goleiros
    
    # Estatísticas avançadas
    xg: float = 0.0
    xa: float = 0.0
    pass_accuracy: float = 0.0
    dribbles_completed: int = 0
    fouls_committed: int = 0
    
    # Rating do jogo (0-10)
    match_rating: float = 6.0
    
    def calculate_match_rating(self) -> float:
        """Calcula o rating baseado na performance"""
        base_rating = 6.0
        
        # Gols e assistências
        base_rating += (self.goals * 1.5)
        base_rating += (self.assists * 1.2)
        
        # Estatísticas positivas
        base_rating += (self.shots_on_target * 0.3)
        base_rating += (self.key_passes * 0.2)
        base_rating += (self.tackles * 0.15)
        base_rating += (self.interceptions * 0.15)
        
        # Para goleiros
        if self.saves > 0:
            base_rating += (self.saves * 0.3)
            if self.saves >= 5:
                base_rating += 1.0  # Bônus por muitas defesas
        
        # Penalidades
        base_rating -= (self.yellow_cards * 0.3)
        base_rating -= (self.red_cards * 2.0)
        
        # Limitar entre 0 e 10
        self.match_rating = max(0.0, min(10.0, base_rating))
        return self.match_rating


@dataclass
class TeamLineup:
    formation: Formation
    players: List[AdvancedPlayer]  # 11 jogadores titulares
    substitutes: List[AdvancedPlayer]  # Banco de reservas
    
    def get_team_rating(self) -> float:
        """Calcula rating médio do time titular"""
        if not self.players:
            return 50.0
        
        total_rating = sum(player.get_effective_overall() for player in self.players[:11])
        return total_rating / min(11, len(self.players))
    
    def get_position_strength(self, position_type: str) -> float:
        """Calcula força em uma área específica (attack, midfield, defense)"""
        relevant_players = []
        
        for player in self.players[:11]:
            if position_type == "attack" and player.position in [Position.ST, Position.CF, Position.LW, Position.RW]:
                relevant_players.append(player)
            elif position_type == "midfield" and player.position in [Position.CM, Position.CAM, Position.CDM, Position.LM, Position.RM]:
                relevant_players.append(player)
            elif position_type == "defense" and player.position in [Position.CB, Position.LB, Position.RB]:
                relevant_players.append(player)
            elif position_type == "goalkeeper" and player.position == Position.GK:
                relevant_players.append(player)
        
        if not relevant_players:
            return 50.0
            
        return sum(p.get_effective_overall() for p in relevant_players) / len(relevant_players)


@dataclass
class AdvancedMatchResult:
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int
    
    # Formações usadas
    home_formation: FormationType
    away_formation: FormationType
    
    # Eventos do jogo
    events: List[MatchEvent] = field(default_factory=list)
    
    # Performance dos jogadores
    home_performances: Dict[str, PlayerMatchPerformance] = field(default_factory=dict)
    away_performances: Dict[str, PlayerMatchPerformance] = field(default_factory=dict)
    
    # Estatísticas do jogo
    home_possession: float = 50.0
    away_possession: float = 50.0
    home_shots: int = 0
    away_shots: int = 0
    home_shots_on_target: int = 0
    away_shots_on_target: int = 0
    
    # Metadata
    match_date: date = field(default_factory=date.today)
    attendance: int = 0
    referee: str = ""


class AdvancedMatchSimulator:
    """Simulador avançado de partidas com eventos detalhados"""
    
    def __init__(self):
        self.random_seed = None
        
    def simulate_match(
        self, 
        home_lineup: TeamLineup, 
        away_lineup: TeamLineup,
        home_team_name: str,
        away_team_name: str,
        match_date: date = None
    ) -> AdvancedMatchResult:
        """Simula uma partida completa com eventos detalhados"""
        
        if match_date is None:
            match_date = date.today()
        
        # Inicializar resultado
        result = AdvancedMatchResult(
            home_team=home_team_name,
            away_team=away_team_name,
            home_goals=0,
            away_goals=0,
            home_formation=home_lineup.formation.name,
            away_formation=away_lineup.formation.name,
            match_date=match_date
        )
        
        # Calcular vantagens táticas
        home_advantage, away_advantage = calculate_tactical_advantage(
            home_lineup.formation, away_lineup.formation
        )
        
        # Adicionar bônus de mando de campo
        home_advantage *= 1.1
        
        # Calcular força dos times
        home_strength = home_lineup.get_team_rating() * home_advantage
        away_strength = away_lineup.get_team_rating() * away_advantage
        
        # Inicializar performances dos jogadores
        for player in home_lineup.players[:11]:
            result.home_performances[player.id] = PlayerMatchPerformance(
                player_id=player.id,
                minutes_played=90  # Assume que todos jogam 90min por enquanto
            )
            
        for player in away_lineup.players[:11]:
            result.away_performances[player.id] = PlayerMatchPerformance(
                player_id=player.id,
                minutes_played=90
            )
        
        # Simular posse de bola baseada na força dos times
        total_strength = home_strength + away_strength
        result.home_possession = (home_strength / total_strength) * 100
        result.away_possession = 100 - result.home_possession
        
        # Simular eventos do jogo
        self._simulate_match_events(result, home_lineup, away_lineup, home_strength, away_strength)
        
        # Calcular ratings dos jogadores
        for performance in result.home_performances.values():
            performance.calculate_match_rating()
            
        for performance in result.away_performances.values():
            performance.calculate_match_rating()
        
        # Aplicar fadiga e atualizar forma dos jogadores
        self._apply_post_match_effects(home_lineup, away_lineup, result)
        
        return result
    
    def _simulate_match_events(
        self, 
        result: AdvancedMatchResult, 
        home_lineup: TeamLineup, 
        away_lineup: TeamLineup,
        home_strength: float,
        away_strength: float
    ):
        """Simula eventos específicos durante a partida"""
        
        # Calcular número esperado de eventos baseado na força dos times
        total_strength = home_strength + away_strength
        
        # Chutes esperados (baseado na força ofensiva) - Mais realista
        home_attack_strength = home_lineup.get_position_strength("attack")
        away_attack_strength = away_lineup.get_position_strength("attack")
        home_defense_strength = home_lineup.get_position_strength("defense")
        away_defense_strength = away_lineup.get_position_strength("defense")
        
        # Calcular modificador baseado na diferença ataque vs defesa
        home_shot_modifier = max(0.7, min(1.3, home_attack_strength / away_defense_strength))
        away_shot_modifier = max(0.7, min(1.3, away_attack_strength / home_defense_strength))
        
        # Chutes mais realistas: 6-15 por time (média ~10-11)
        expected_home_shots = max(5, int(10 * home_shot_modifier * random.uniform(0.8, 1.2)))
        expected_away_shots = max(5, int(10 * away_shot_modifier * random.uniform(0.8, 1.2)))
        
        result.home_shots = expected_home_shots
        result.away_shots = expected_away_shots
        
        # Simular chutes e gols para o time da casa
        home_goals = self._simulate_team_attacks(
            result, home_lineup, away_lineup, expected_home_shots, True
        )
        
        # Simular chutes e gols para o time visitante  
        away_goals = self._simulate_team_attacks(
            result, away_lineup, home_lineup, expected_away_shots, False
        )
        
        result.home_goals = home_goals
        result.away_goals = away_goals
        
        # Simular outros eventos (cartões, lesões, etc.)
        self._simulate_disciplinary_events(result, home_lineup, away_lineup)
    
    def _simulate_team_attacks(
        self,
        result: AdvancedMatchResult,
        attacking_lineup: TeamLineup,
        defending_lineup: TeamLineup,
        expected_shots: int,
        is_home_team: bool
    ) -> int:
        """Simula ataques de um time específico"""
        goals = 0
        shots_on_target = 0
        team_name = result.home_team if is_home_team else result.away_team
        performances = result.home_performances if is_home_team else result.away_performances
        
        # Obter jogadores atacantes
        attacking_players = [p for p in attacking_lineup.players[:11] 
                           if p.position in [Position.ST, Position.CF, Position.LW, Position.RW, Position.CAM]]
        
        if not attacking_players:
            attacking_players = attacking_lineup.players[:11]  # Fallback
        
        # Força defensiva do adversário
        defending_strength = defending_lineup.get_position_strength("defense")
        goalkeeper_strength = defending_lineup.get_position_strength("goalkeeper")
        
        for shot_num in range(expected_shots):
            # Escolher jogador que chuta (atacantes têm mais chance)
            shooter = random.choice(attacking_players)
            minute = random.randint(1, 90)
            
            # Calcular probabilidade de acertar o alvo (balanceado)
            shooter_ability = (shooter.attributes.shooting or 50) + (shooter.attributes.finishing or 50)
            shot_accuracy = max(0.18, min(0.42, (shooter_ability / 200) * random.uniform(0.8, 1.2)))
            
            if random.random() < shot_accuracy:
                # Chute no alvo
                shots_on_target += 1
                performances[shooter.id].shots_on_target += 1
                
                # Adicionar evento
                result.events.append(MatchEvent(
                    minute=minute,
                    event_type=EventType.SHOT_ON_TARGET,
                    player_id=shooter.id,
                    team_name=team_name,
                    description=f"{shooter.name} shot on target"
                ))
                
                # Calcular probabilidade de gol (otimizado para ~2.5 gols/jogo)
                goal_probability = max(0.08, min(0.28, (shooter_ability / 240) / (goalkeeper_strength / 80)))
                
                if random.random() < goal_probability:
                    # GOL!
                    goals += 1
                    performances[shooter.id].goals += 1
                    
                    # Possível assistência
                    assisting_player = None
                    if random.random() < 0.6:  # 60% chance de assistência
                        midfielders = [p for p in attacking_lineup.players[:11] 
                                     if p.position in [Position.CM, Position.CAM, Position.LM, Position.RM]]
                        if midfielders:
                            assisting_player = random.choice(midfielders)
                            performances[assisting_player.id].assists += 1
                    
                    # Adicionar evento de gol
                    description = f"{shooter.name} scores!"
                    if assisting_player:
                        description += f" (Assisted by {assisting_player.name})"
                    
                    result.events.append(MatchEvent(
                        minute=minute,
                        event_type=EventType.GOAL,
                        player_id=shooter.id,
                        team_name=team_name,
                        description=description,
                        assisted_by=assisting_player.id if assisting_player else None,
                        rating_impact=1.5
                    ))
                    
                    if assisting_player:
                        result.events.append(MatchEvent(
                            minute=minute,
                            event_type=EventType.ASSIST,
                            player_id=assisting_player.id,
                            team_name=team_name,
                            description=f"{assisting_player.name} provides assist",
                            rating_impact=1.0
                        ))
                else:
                    # Defesa do goleiro
                    goalkeeper = next((p for p in defending_lineup.players[:11] if p.position == Position.GK), None)
                    if goalkeeper:
                        defending_performances = result.away_performances if is_home_team else result.home_performances
                        defending_performances[goalkeeper.id].saves += 1
                        
                        result.events.append(MatchEvent(
                            minute=minute,
                            event_type=EventType.SAVE,
                            player_id=goalkeeper.id,
                            team_name=result.away_team if is_home_team else result.home_team,
                            description=f"{goalkeeper.name} makes a save",
                            rating_impact=0.3
                        ))
            else:
                # Chute para fora
                result.events.append(MatchEvent(
                    minute=minute,
                    event_type=EventType.SHOT_OFF_TARGET,
                    player_id=shooter.id,
                    team_name=team_name,
                    description=f"{shooter.name} shot off target",
                    rating_impact=-0.1
                ))
            
            performances[shooter.id].shots += 1
        
        # Atualizar estatísticas do resultado
        if is_home_team:
            result.home_shots_on_target = shots_on_target
        else:
            result.away_shots_on_target = shots_on_target
        
        return goals
    
    def _simulate_disciplinary_events(
        self,
        result: AdvancedMatchResult,
        home_lineup: TeamLineup,
        away_lineup: TeamLineup
    ):
        """Simula cartões e outros eventos disciplinares"""
        
        all_players = home_lineup.players[:11] + away_lineup.players[:11]
        
        # Simular cartões amarelos (2-6 por jogo)
        yellow_cards = random.randint(2, 6)
        
        for _ in range(yellow_cards):
            player = random.choice(all_players)
            minute = random.randint(10, 90)
            
            is_home = player in home_lineup.players
            team_name = result.home_team if is_home else result.away_team
            performances = result.home_performances if is_home else result.away_performances
            
            performances[player.id].yellow_cards += 1
            
            result.events.append(MatchEvent(
                minute=minute,
                event_type=EventType.YELLOW_CARD,
                player_id=player.id,
                team_name=team_name,
                description=f"{player.name} receives yellow card",
                rating_impact=-0.3
            ))
        
        # Simular cartões vermelhos (0-1 por jogo, raro)
        if random.random() < 0.15:  # 15% chance de cartão vermelho
            player = random.choice(all_players)
            minute = random.randint(20, 85)
            
            is_home = player in home_lineup.players
            team_name = result.home_team if is_home else result.away_team
            performances = result.home_performances if is_home else result.away_performances
            
            performances[player.id].red_cards += 1
            
            result.events.append(MatchEvent(
                minute=minute,
                event_type=EventType.RED_CARD,
                player_id=player.id,
                team_name=team_name,
                description=f"{player.name} receives red card",
                rating_impact=-2.0
            ))
    
    def _apply_post_match_effects(
        self,
        home_lineup: TeamLineup,
        away_lineup: TeamLineup,
        result: AdvancedMatchResult
    ):
        """Aplica efeitos pós-jogo (fadiga, forma, etc.)"""
        
        # Aplicar fadiga e atualizar forma para jogadores da casa
        for player in home_lineup.players[:11]:
            performance = result.home_performances[player.id]
            
            # Aplicar fadiga
            player.apply_fatigue(performance.minutes_played)
            
            # Atualizar forma baseada na performance
            player.update_form(int(performance.match_rating))
            
            # Verificar risco de lesão
            if player.check_injury_risk():
                player.get_injured()
                result.events.append(MatchEvent(
                    minute=random.randint(70, 90),
                    event_type=EventType.INJURY,
                    player_id=player.id,
                    team_name=result.home_team,
                    description=f"{player.name} gets injured",
                    rating_impact=-0.5
                ))
        
        # Mesmo para jogadores visitantes
        for player in away_lineup.players[:11]:
            performance = result.away_performances[player.id]
            
            player.apply_fatigue(performance.minutes_played)
            player.update_form(int(performance.match_rating))
            
            if player.check_injury_risk():
                player.get_injured()
                result.events.append(MatchEvent(
                    minute=random.randint(70, 90),
                    event_type=EventType.INJURY,
                    player_id=player.id,
                    team_name=result.away_team,
                    description=f"{player.name} gets injured",
                    rating_impact=-0.5
                ))