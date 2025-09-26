from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from ...models.player import Position, AdvancedPlayer


class FormationType(Enum):
    F_4_4_2 = "4-4-2"
    F_4_3_3 = "4-3-3"
    F_4_2_3_1 = "4-2-3-1"
    F_3_5_2 = "3-5-2"
    F_5_3_2 = "5-3-2"
    F_4_5_1 = "4-5-1"
    F_3_4_3 = "3-4-3"


class PlayStyle(Enum):
    ATTACKING = "Attacking"
    BALANCED = "Balanced"
    DEFENSIVE = "Defensive"
    COUNTER_ATTACK = "Counter Attack"
    POSSESSION = "Possession"
    HIGH_PRESS = "High Press"


@dataclass
class FormationPosition:
    """Define uma posição específica na formação"""
    position: Position
    x: float  # 0-100, posição horizontal no campo
    y: float  # 0-100, posição vertical no campo (0=defesa, 100=ataque)
    importance: float = 1.0  # Multiplicador de importância da posição


@dataclass
class Formation:
    """Representa uma formação tática completa"""
    name: FormationType
    positions: List[FormationPosition]
    compatible_styles: List[PlayStyle]
    
    # Modificadores táticos (0.8 a 1.2)
    attack_modifier: float = 1.0
    defense_modifier: float = 1.0
    midfield_modifier: float = 1.0
    
    # Instruções específicas
    instructions: Optional[Dict[str, float]] = None
    
    def __post_init__(self):
        if self.instructions is None:
            self.instructions = {
                "tempo": 1.0,          # Velocidade do jogo
                "width": 1.0,          # Largura do jogo
                "pressing": 1.0,       # Intensidade da marcação
                "directness": 1.0,     # Jogo direto vs elaborado
                "risk_taking": 1.0     # Assumir riscos vs conservador
            }


# Definir as formações disponíveis
FORMATIONS: Dict[FormationType, Formation] = {
    
    FormationType.F_4_4_2: Formation(
        name=FormationType.F_4_4_2,
        positions=[
            # Goleiro
            FormationPosition(Position.GK, 50, 5),
            
            # Defesa (4)
            FormationPosition(Position.LB, 15, 20),
            FormationPosition(Position.CB, 35, 15),
            FormationPosition(Position.CB, 65, 15),
            FormationPosition(Position.RB, 85, 20),
            
            # Meio-campo (4)
            FormationPosition(Position.LM, 20, 50),
            FormationPosition(Position.CM, 40, 45),
            FormationPosition(Position.CM, 60, 45),
            FormationPosition(Position.RM, 80, 50),
            
            # Ataque (2)
            FormationPosition(Position.ST, 40, 80),
            FormationPosition(Position.ST, 60, 80)
        ],
        attack_modifier=1.05,
        defense_modifier=1.0,
        midfield_modifier=0.95,
        compatible_styles=[PlayStyle.BALANCED, PlayStyle.COUNTER_ATTACK],
        instructions={
            "tempo": 1.0,
            "width": 1.1,
            "pressing": 0.9,
            "directness": 1.1,
            "risk_taking": 1.0
        }
    ),
    
    FormationType.F_4_3_3: Formation(
        name=FormationType.F_4_3_3,
        positions=[
            # Goleiro
            FormationPosition(Position.GK, 50, 5),
            
            # Defesa (4)
            FormationPosition(Position.LB, 15, 20),
            FormationPosition(Position.CB, 35, 15),
            FormationPosition(Position.CB, 65, 15),
            FormationPosition(Position.RB, 85, 20),
            
            # Meio-campo (3)
            FormationPosition(Position.CDM, 50, 35),
            FormationPosition(Position.CM, 35, 50),
            FormationPosition(Position.CM, 65, 50),
            
            # Ataque (3)
            FormationPosition(Position.LW, 20, 75),
            FormationPosition(Position.ST, 50, 80),
            FormationPosition(Position.RW, 80, 75)
        ],
        attack_modifier=1.1,
        defense_modifier=0.95,
        midfield_modifier=1.05,
        compatible_styles=[PlayStyle.ATTACKING, PlayStyle.HIGH_PRESS, PlayStyle.POSSESSION],
        instructions={
            "tempo": 1.1,
            "width": 1.2,
            "pressing": 1.2,
            "directness": 0.9,
            "risk_taking": 1.2
        }
    ),
    
    FormationType.F_4_2_3_1: Formation(
        name=FormationType.F_4_2_3_1,
        positions=[
            # Goleiro
            FormationPosition(Position.GK, 50, 5),
            
            # Defesa (4)
            FormationPosition(Position.LB, 15, 20),
            FormationPosition(Position.CB, 35, 15),
            FormationPosition(Position.CB, 65, 15),
            FormationPosition(Position.RB, 85, 20),
            
            # Meio-campo defensivo (2)
            FormationPosition(Position.CDM, 40, 35),
            FormationPosition(Position.CDM, 60, 35),
            
            # Meio-campo ofensivo (3)
            FormationPosition(Position.LW, 20, 65),
            FormationPosition(Position.CAM, 50, 60),
            FormationPosition(Position.RW, 80, 65),
            
            # Ataque (1)
            FormationPosition(Position.ST, 50, 80)
        ],
        attack_modifier=1.0,
        defense_modifier=1.1,
        midfield_modifier=1.1,
        compatible_styles=[PlayStyle.BALANCED, PlayStyle.POSSESSION, PlayStyle.COUNTER_ATTACK],
        instructions={
            "tempo": 0.95,
            "width": 1.0,
            "pressing": 1.0,
            "directness": 0.85,
            "risk_taking": 0.9
        }
    ),
    
    FormationType.F_5_3_2: Formation(
        name=FormationType.F_5_3_2,
        positions=[
            # Goleiro
            FormationPosition(Position.GK, 50, 5),
            
            # Defesa (5)
            FormationPosition(Position.LB, 10, 25),
            FormationPosition(Position.CB, 30, 15),
            FormationPosition(Position.CB, 50, 10),
            FormationPosition(Position.CB, 70, 15),
            FormationPosition(Position.RB, 90, 25),
            
            # Meio-campo (3)
            FormationPosition(Position.CM, 30, 50),
            FormationPosition(Position.CM, 50, 45),
            FormationPosition(Position.CM, 70, 50),
            
            # Ataque (2)
            FormationPosition(Position.ST, 40, 75),
            FormationPosition(Position.ST, 60, 75)
        ],
        attack_modifier=0.85,
        defense_modifier=1.2,
        midfield_modifier=0.95,
        compatible_styles=[PlayStyle.DEFENSIVE, PlayStyle.COUNTER_ATTACK],
        instructions={
            "tempo": 0.8,
            "width": 0.9,
            "pressing": 0.7,
            "directness": 1.3,
            "risk_taking": 0.6
        }
    ),
    
    FormationType.F_3_5_2: Formation(
        name=FormationType.F_3_5_2,
        positions=[
            # Goleiro
            FormationPosition(Position.GK, 50, 5),
            
            # Defesa (3)
            FormationPosition(Position.CB, 30, 20),
            FormationPosition(Position.CB, 50, 15),
            FormationPosition(Position.CB, 70, 20),
            
            # Meio-campo (5)
            FormationPosition(Position.LM, 10, 50),
            FormationPosition(Position.CM, 30, 45),
            FormationPosition(Position.CM, 50, 40),
            FormationPosition(Position.CM, 70, 45),
            FormationPosition(Position.RM, 90, 50),
            
            # Ataque (2)
            FormationPosition(Position.ST, 40, 75),
            FormationPosition(Position.ST, 60, 75)
        ],
        attack_modifier=1.0,
        defense_modifier=0.9,
        midfield_modifier=1.2,
        compatible_styles=[PlayStyle.POSSESSION, PlayStyle.ATTACKING, PlayStyle.BALANCED],
        instructions={
            "tempo": 1.0,
            "width": 1.3,
            "pressing": 1.1,
            "directness": 0.8,
            "risk_taking": 1.1
        }
    )
}


def get_formation_effectiveness(formation: Formation, players: List[AdvancedPlayer]) -> float:
    """
    Calcula a efetividade de uma formação baseada nos jogadores disponíveis
    Retorna valor de 0.5 a 1.5
    """
    if len(players) != 11:
        return 0.5
    
    effectiveness = 1.0
    
    # Verificar se os jogadores estão nas posições certas
    for i, formation_pos in enumerate(formation.positions):
        if i >= len(players):
            break
            
        player = players[i]
        required_position = formation_pos.position
        
        # Calcular adaptação do jogador à posição
        position_rating = player.get_position_rating(required_position)
        position_effectiveness = position_rating / player.get_effective_overall()
        
        # Aplicar peso da importância da posição
        weighted_effectiveness = position_effectiveness * formation_pos.importance
        effectiveness *= weighted_effectiveness
    
    # Normalizar para faixa 0.5-1.5
    return max(0.5, min(1.5, effectiveness))


def recommend_formation_for_team(players: List[AdvancedPlayer]) -> FormationType:
    """
    Recomenda a melhor formação baseada no elenco disponível
    """
    best_formation = FormationType.F_4_4_2
    best_effectiveness = 0.0
    
    for formation_type, formation in FORMATIONS.items():
        # Simular lineup básico
        effectiveness = get_formation_effectiveness(formation, players[:11])
        
        if effectiveness > best_effectiveness:
            best_effectiveness = effectiveness
            best_formation = formation_type
    
    return best_formation


def calculate_tactical_advantage(home_formation: Formation, away_formation: Formation) -> Tuple[float, float]:
    """
    Calcula vantagens táticas entre duas formações
    Retorna (home_advantage, away_advantage)
    """
    # Comparar forças em diferentes áreas do campo
    home_attack_vs_away_defense = home_formation.attack_modifier / away_formation.defense_modifier
    away_attack_vs_home_defense = away_formation.attack_modifier / home_formation.defense_modifier
    
    # Considerar compatibilidade de estilos
    style_factor = 1.0
    
    # Formações mais defensivas tendem a anular formações ofensivas
    if (home_formation.defense_modifier > 1.1 and away_formation.attack_modifier > 1.1) or \
       (away_formation.defense_modifier > 1.1 and home_formation.attack_modifier > 1.1):
        style_factor = 0.9  # Reduz efetividade ofensiva
    
    home_advantage = max(0.8, min(1.2, home_attack_vs_away_defense * style_factor))
    away_advantage = max(0.8, min(1.2, away_attack_vs_home_defense * style_factor))
    
    return home_advantage, away_advantage