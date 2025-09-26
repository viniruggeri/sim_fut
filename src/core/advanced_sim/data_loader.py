#!/usr/bin/env python3
"""
Carregador de dados dos times a partir dos arquivos JSON
Converte dados reais em objetos AdvancedPlayer e TeamLineup para simulação
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

# Adicionar src ao path
import sys
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))

from core.advanced_sim.models.player import AdvancedPlayer, Position, PlayerAttributes
from core.advanced_sim.stats.tatics.formations import FormationType, FORMATIONS
from core.advanced_sim.simulation.advanced_match import TeamLineup


@dataclass
class TeamData:
    """Dados básicos de um time carregados do JSON"""
    name: str
    attack_avg: float
    midfield_avg: float
    defense_avg: float
    goalkeeper_avg: float
    players: List[Dict]


class LeagueDataLoader:
    """Carregador de dados das ligas a partir dos arquivos JSON"""
    
    # Mapeamento de setores para posições específicas
    POSITION_MAPPING = {
        'Goleiro': [Position.GK],
        'Defesa': [Position.CB, Position.LB, Position.RB],
        'Meio': [Position.CDM, Position.CM, Position.CAM, Position.LM, Position.RM],
        'Ataque': [Position.LW, Position.ST, Position.RW]
    }
    
    # Formações padrão por qualidade do time
    FORMATION_BY_QUALITY = {
        (85, 100): FormationType.F_4_3_3,    # Times de elite
        (75, 84): FormationType.F_4_4_2,     # Times médio-altos
        (65, 74): FormationType.F_4_3_3,     # Times médios
        (0, 64): FormationType.F_4_4_2       # Times mais fracos
    }
    
    def __init__(self, data_dir: Path | None = None):
        """Inicializa o carregador com o diretório de dados"""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent.parent / "data" / "processed" / "leagues"
        self.data_dir = data_dir
        
    def load_league(self, league_name: str) -> Dict[str, TeamData]:
        """Carrega dados de uma liga específica"""
        league_file = self.data_dir / f"{league_name}_2025.json"
        
        if not league_file.exists():
            raise FileNotFoundError(f"Arquivo da liga não encontrado: {league_file}")
            
        with open(league_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        teams = {}
        for team_name, team_info in data['times'].items():
            # Converter jogadores para lista com informações adicionais
            players = []
            for player_name, player_info in team_info['jogadores'].items():
                player_data = player_info.copy()
                player_data['name'] = player_name.replace(' -', '')  # Remove sufixo
                players.append(player_data)
            
            teams[team_name] = TeamData(
                name=team_name,
                attack_avg=team_info['medias']['ataque'],
                midfield_avg=team_info['medias']['meio'], 
                defense_avg=team_info['medias']['defesa'],
                goalkeeper_avg=team_info['medias']['goleiro'],
                players=players
            )
        
        return teams
    
    def _map_setor_to_position(self, setor: str, overall: int) -> Position:
        """Mapeia setor genérico para posição específica baseada no overall"""
        possible_positions = self.POSITION_MAPPING.get(setor, [Position.CM])
        
        if setor == 'Defesa':
            # Jogadores melhores tendem a ser CB, piores LB/RB
            if overall >= 80:
                return random.choice([Position.CB, Position.CB, Position.LB, Position.RB])
            else:
                return random.choice([Position.CB, Position.LB, Position.RB])
                
        elif setor == 'Meio':
            # Distribuição baseada no overall
            if overall >= 85:
                return random.choice([Position.CAM, Position.CM, Position.CDM])
            elif overall >= 75:
                return random.choice([Position.CM, Position.CDM, Position.LM, Position.RM])
            else:
                return random.choice([Position.CM, Position.CDM])
                
        elif setor == 'Ataque':
            # Atacantes melhores são ST, outros nas pontas
            if overall >= 82:
                return random.choice([Position.ST, Position.ST, Position.LW, Position.RW])
            else:
                return random.choice([Position.LW, Position.RW, Position.ST])
        
        # Goleiro ou fallback
        return possible_positions[0]
    
    def _create_player_attributes(self, player_data: Dict, overall: int, setor: str) -> PlayerAttributes:
        """Cria atributos detalhados do jogador baseado nos dados reais"""
        # Usar dados reais do overall em vez de inventar
        attributes = PlayerAttributes()
        
        # Variação pequena baseada no overall real
        base_variance = random.randint(-5, 5)
        
        if setor == 'Goleiro':
            attributes.goalkeeping = overall
            # Goleiros têm outros atributos proporcionais mas menores
            attributes.pace = max(30, overall - 25)
            attributes.shooting = max(30, overall - 35)
            attributes.passing = max(30, overall - 10)
            attributes.dribbling = max(30, overall - 20)
            attributes.defending = max(30, overall - 15)
            attributes.physical = max(30, overall - 5)
            
        elif setor == 'Defesa':
            # Defensores: defending e physical altos, baseados no overall real
            attributes.defending = min(99, overall + 2)
            attributes.physical = min(99, overall)
            attributes.passing = max(30, overall - 8)
            attributes.pace = max(30, overall - 10)
            attributes.shooting = max(30, overall - 20)
            attributes.dribbling = max(30, overall - 12)
            
        elif setor == 'Meio':
            # Meio-campistas: passing e dribbling altos
            attributes.passing = min(99, overall + 3)
            attributes.dribbling = min(99, overall)
            attributes.pace = max(30, overall - 5)
            attributes.shooting = max(30, overall - 10)
            attributes.defending = max(30, overall - 8)
            attributes.physical = max(30, overall - 3)
            
        elif setor == 'Ataque':
            # Atacantes: shooting e pace altos
            attributes.shooting = min(99, overall + 5)
            attributes.pace = min(99, overall + 2)
            attributes.dribbling = min(99, overall)
            attributes.passing = max(30, overall - 5)
            attributes.defending = max(30, overall - 20)
            attributes.physical = max(30, overall - 8)
        
        return attributes
    
    def convert_team_to_lineup(self, team_data: TeamData) -> TeamLineup:
        """Converte dados do time em TeamLineup para simulação"""
        
        # Calcular overall médio do time para escolher formação
        team_overall = (team_data.attack_avg + team_data.midfield_avg + 
                       team_data.defense_avg + team_data.goalkeeper_avg) / 4
        
        # Escolher formação baseada na qualidade
        formation = FormationType.F_4_3_3  # Padrão
        for (min_qual, max_qual), form in self.FORMATION_BY_QUALITY.items():
            if min_qual <= team_overall <= max_qual:
                formation = form
                break
        
        # Converter jogadores
        advanced_players = []
        for player_data in team_data.players:
            position = self._map_setor_to_position(player_data['setor'], player_data['overall'])
            attributes = self._create_player_attributes(player_data, player_data['overall'], player_data['setor'])
            
            # Usar dados reais do jogador
            player = AdvancedPlayer(
                name=player_data['name'],
                age=random.randint(18, 35),  # Idade aleatória (não temos no JSON)
                position=position,
                current_overall=player_data['overall'],  # Overall real do FIFA
                potential=player_data['potential'],       # Potential real do FIFA
                attributes=attributes,
                current_form=random.randint(60, 90),  # Forma inicial boa
                morale=random.randint(70, 95),        # Moral inicial alta
                fitness=random.randint(90, 100)       # Fitness inicial máxima
            )
            
            advanced_players.append(player)
        
        # Separar titulares dos reservas (11 melhores são titulares)
        advanced_players.sort(key=lambda p: p.current_overall, reverse=True)
        starters = advanced_players[:11]
        substitutes = advanced_players[11:18] if len(advanced_players) > 11 else []
        
        return TeamLineup(
            formation=FORMATIONS[formation],
            players=starters,
            substitutes=substitutes
        )
    
    def load_league_for_simulation(self, league_name: str) -> Dict[str, TeamLineup]:
        """Carrega uma liga completa pronta para simulação"""
        teams_data = self.load_league(league_name)
        
        league_lineups = {}
        for team_name, team_data in teams_data.items():
            lineup = self.convert_team_to_lineup(team_data)
            league_lineups[team_name] = lineup
            
        return league_lineups
    
    def get_available_leagues(self) -> List[str]:
        """Retorna lista das ligas disponíveis"""
        leagues = []
        for file_path in self.data_dir.glob("*_2025.json"):
            league_name = file_path.stem.replace("_2025", "")
            leagues.append(league_name)
        return leagues


if __name__ == "__main__":
    # Teste do carregador
    loader = LeagueDataLoader()
    
    print("🔍 Ligas disponíveis:")
    for league in loader.get_available_leagues():
        print(f"  • {league}")
    
    print(f"\n📊 Carregando Premier League...")
    teams = loader.load_league_for_simulation("premier_league")
    
    print(f"✅ {len(teams)} times carregados!")
    
    # Mostrar alguns exemplos
    for i, (team_name, lineup) in enumerate(teams.items()):
        if i < 3:  # Primeiros 3 times
            print(f"\n🏆 {team_name}:")
            print(f"   Formação: {lineup.formation.name}")
            print(f"   Overall médio: {lineup.get_team_rating():.1f}")
            print(f"   Titulares: {len(lineup.players)}, Reservas: {len(lineup.substitutes)}")