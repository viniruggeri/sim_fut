from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime
import uuid

class Position(Enum):
    GK = "Goalkeeper"
    CB = "Centre-Back"
    LB = "Left-Back" 
    RB = "Right-Back"
    CDM = "Defensive Midfielder"
    CM = "Central Midfielder"
    CAM = "Attacking Midfielder"
    LW = "Left Winger"
    RW = "Right Winger"
    CF = "Centre Forward"
    ST = "Striker"
    
@dataclass
class PlayerAttributes:
    pace: int
    shooting: int
    passing: int
    driblling: int
    defending: int
    physical: int
    
    goalkeeping: Optional[int]= None
    crossing: Optional[int]= None
    finishing: Optional[int]= None
    heading: Optional[int]= None
    
@dataclass
class SeasonStats:
    matches_played: int = 0
    minutes_played: int = 0
    goals: int = 0
    assists: int = 0
    
    xg: float = 0.0 
    xa: float = 0.0
    shots: int = 0
    shots_on_target: int = 0
    key_passes: int = 0
    tackles: int = 0
    interceptions: int = 0
    
    #por 90 min
    @property
    def goals_per_90(self) -> float:
        if self.minutes_played == 0:
            return 0
        return (self.minutes_played * 90) / self.minutes_played
    
    @property
    def assists_per_90(self) -> float:
        if self.minutes_played == 0:
            return 0
        return (self.assists * 90) / self.minutes_played

@dataclass
class AdvancedPlayer:
    id: str = field(default_factory=lambda: str(uuid.uuid4))
    name: str = ""
    age: int = 16
    position = Position = Position.CAM
    preferred_position: List[Position] = field(default_factory=list)
    
    #Ratings
    current_overall: int = 50
    potential: int = 50
    
    attributes: PlayerAttributes = field(default_factory=PlayerAttributes)