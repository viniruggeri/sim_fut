from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime, date
import uuid
import random
import numpy as np

class Position(Enum):
    GK = "Goalkeeper"
    CB = "Centre-Back"
    LB = "Left-Back" 
    RB = "Right-Back"
    CDM = "Defensive Midfielder"
    CM = "Central Midfielder"
    CAM = "Attacking Midfielder"
    LM = "Left Midfielder"
    RM = "Right Midfielder"
    LW = "Left Winger"
    RW = "Right Winger"
    CF = "Centre Forward"
    ST = "Striker"

class InjuryType(Enum):
    MINOR = "Minor"      # 1-2 weeks
    MODERATE = "Moderate" # 3-6 weeks
    MAJOR = "Major"      # 2-4 months
    SEVERE = "Severe"    # 6+ months

@dataclass
class Injury:
    type: InjuryType
    start_date: date
    expected_return: date
    description: str
    
@dataclass
class PlayerAttributes:
    # Atributos principais do FIFA
    pace: int = 50
    shooting: int = 50
    passing: int = 50
    dribbling: int = 50
    defending: int = 50
    physical: int = 50
    
    # Atributos específicos de goleiro
    goalkeeping: Optional[int] = None
    
    # Atributos detalhados
    crossing: Optional[int] = None
    finishing: Optional[int] = None
    heading: Optional[int] = None
    short_passing: Optional[int] = None
    volleys: Optional[int] = None
    long_passing: Optional[int] = None
    ball_control: Optional[int] = None
    acceleration: Optional[int] = None
    sprint_speed: Optional[int] = None
    agility: Optional[int] = None
    reactions: Optional[int] = None
    balance: Optional[int] = None
    shot_power: Optional[int] = None
    jumping: Optional[int] = None
    stamina: Optional[int] = None
    strength: Optional[int] = None
    long_shots: Optional[int] = None
    aggression: Optional[int] = None
    interceptions: Optional[int] = None
    positioning: Optional[int] = None
    vision: Optional[int] = None
    penalties: Optional[int] = None
    composure: Optional[int] = None
    
@dataclass
class SeasonStats:
    matches_played: int = 0
    minutes_played: int = 0
    goals: int = 0
    assists: int = 0
    
    # Estatísticas avançadas
    xg: float = 0.0  # Expected Goals
    xa: float = 0.0  # Expected Assists
    shots: int = 0
    shots_on_target: int = 0
    key_passes: int = 0
    tackles: int = 0
    interceptions_made: int = 0
    
    # Cartões
    yellow_cards: int = 0
    red_cards: int = 0
    
    # Para goleiros
    saves: int = 0
    clean_sheets: int = 0
    goals_conceded: int = 0
    
    # Por 90 minutos
    @property
    def goals_per_90(self) -> float:
        if self.minutes_played == 0:
            return 0
        return (self.goals * 90) / self.minutes_played
    
    @property
    def assists_per_90(self) -> float:
        if self.minutes_played == 0:
            return 0
        return (self.assists * 90) / self.minutes_played
        
    @property
    def xg_per_90(self) -> float:
        if self.minutes_played == 0:
            return 0
        return (self.xg * 90) / self.minutes_played

@dataclass
class AdvancedPlayer:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    age: int = 16
    position: Position = Position.CAM
    preferred_positions: List[Position] = field(default_factory=list)
    
    # Ratings
    current_overall: int = 50
    potential: int = 50
    
    # Atributos
    attributes: PlayerAttributes = field(default_factory=PlayerAttributes)
    
    # Sistema de forma
    current_form: int = 50  # 0-100, afeta performance temporariamente
    morale: int = 50       # 0-100, moral do jogador
    fitness: int = 100     # 0-100, condição física
    
    # Sistema de lesões
    is_injured: bool = False
    current_injury: Optional[Injury] = None
    injury_proneness: int = 50  # 0-100, tendência a se lesionar
    
    # Estatísticas da temporada
    season_stats: SeasonStats = field(default_factory=SeasonStats)
    
    # Histórico
    market_value: int = 1000000  # Em euros
    contract_expires: Optional[date] = None
    
    def get_effective_overall(self) -> int:
        """Calcula o overall efetivo considerando forma, moral e fitness"""
        base = self.current_overall
        
        # Fator de forma (-10 a +10)
        form_bonus = (self.current_form - 50) * 0.2
        
        # Fator de moral (-5 a +5)  
        morale_bonus = (self.morale - 50) * 0.1
        
        # Fator de fitness (-15 a 0)
        fitness_penalty = max(0, (100 - self.fitness) * 0.15)
        
        effective = base + form_bonus + morale_bonus - fitness_penalty
        return max(30, min(99, int(effective)))
    
    def get_position_rating(self, position: Position) -> int:
        """Calcula rating do jogador em uma posição específica"""
        base_rating = self.get_effective_overall()
        
        if position == self.position:
            return base_rating
        elif position in self.preferred_positions:
            return max(30, base_rating - 5)  # -5 fora da posição preferida
        else:
            # Penalty maior para posições muito diferentes
            penalty = self._calculate_position_penalty(position)
            return max(30, base_rating - penalty)
    
    def _calculate_position_penalty(self, position: Position) -> int:
        """Calcula penalidade por jogar fora de posição"""
        # Definir grupos de posições similares
        goalkeeper = {Position.GK}
        defense = {Position.CB, Position.LB, Position.RB}
        midfield = {Position.CDM, Position.CM, Position.CAM, Position.LM, Position.RM}
        attack = {Position.LW, Position.RW, Position.CF, Position.ST}
        
        current_group = self._get_position_group(self.position)
        target_group = self._get_position_group(position)
        
        if current_group == target_group:
            return 8  # Mesmo grupo, penalty menor
        elif (current_group == midfield and target_group == attack) or \
             (current_group == attack and target_group == midfield):
            return 12  # Meio/ataque, penalty moderado
        else:
            return 20  # Grupos muito diferentes, penalty alto
    
    def _get_position_group(self, position: Position) -> set:
        """Retorna o grupo da posição"""
        goalkeeper = {Position.GK}
        defense = {Position.CB, Position.LB, Position.RB}
        midfield = {Position.CDM, Position.CM, Position.CAM, Position.LM, Position.RM}
        attack = {Position.LW, Position.RW, Position.CF, Position.ST}
        
        for group in [goalkeeper, defense, midfield, attack]:
            if position in group:
                return group
        return midfield  # Default
    
    def apply_fatigue(self, minutes_played: int):
        """Aplica fadiga baseada nos minutos jogados"""
        if minutes_played > 0:
            # Reduz fitness baseado nos minutos (mais minutos = mais fadiga)
            fatigue = max(1, minutes_played / 15)  # ~6 pontos para 90min
            self.fitness = max(0, int(self.fitness - fatigue))
    
    def recover_fitness(self, days_rest: int = 1):
        """Recupera fitness durante descanso"""
        recovery = min(15 * days_rest, 100 - self.fitness)
        self.fitness = min(100, int(self.fitness + recovery))
    
    def update_form(self, performance: int):
        """Atualiza forma baseada na performance do jogo (0-10)"""
        # Performance boa aumenta forma, ruim diminui
        if performance >= 7:
            self.current_form = min(100, self.current_form + random.randint(2, 5))
        elif performance <= 4:
            self.current_form = max(0, self.current_form - random.randint(2, 5))
        else:
            # Performance mediana, pequena mudança aleatória
            change = random.randint(-2, 2)
            self.current_form = max(0, min(100, self.current_form + change))
    
    def check_injury_risk(self) -> bool:
        """Verifica se o jogador se lesiona baseado em vários fatores"""
        base_risk = self.injury_proneness / 1000  # Base 0-0.1
        
        # Fitness baixo aumenta risco
        fitness_risk = max(0, (100 - self.fitness) / 2000)
        
        # Idade aumenta risco
        age_risk = max(0, (self.age - 30) / 1000) if self.age > 30 else 0
        
        total_risk = base_risk + fitness_risk + age_risk
        return random.random() < total_risk
    
    def get_injured(self, severity: Optional[InjuryType] = None):
        """Aplica lesão ao jogador"""
        if not severity:
            # Determinar severidade aleatoriamente (lesões menores são mais comuns)
            rand = random.random()
            if rand < 0.6:
                severity = InjuryType.MINOR
            elif rand < 0.85:
                severity = InjuryType.MODERATE  
            elif rand < 0.95:
                severity = InjuryType.MAJOR
            else:
                severity = InjuryType.SEVERE
        
        # Calcular tempo de recuperação
        recovery_days = {
            InjuryType.MINOR: random.randint(7, 14),
            InjuryType.MODERATE: random.randint(21, 42), 
            InjuryType.MAJOR: random.randint(60, 120),
            InjuryType.SEVERE: random.randint(180, 300)
        }
        
        start_date = date.today()
        days_out = recovery_days[severity]
        
        self.is_injured = True
        self.current_injury = Injury(
            type=severity,
            start_date=start_date,
            expected_return=date.fromordinal(start_date.toordinal() + days_out),
            description=f"{severity.value} injury"
        )
        
        # Fitness reduzido durante lesão
        self.fitness = max(20, self.fitness - 30)
    
    def recover_from_injury(self):
        """Recupera jogador de lesão"""
        self.is_injured = False
        self.current_injury = None
        # Fitness ainda baixo após lesão, precisa treinar para recuperar
        self.fitness = max(self.fitness, 60)
    
    def can_play(self) -> bool:
        """Verifica se o jogador pode jogar"""
        return not self.is_injured and self.fitness > 30