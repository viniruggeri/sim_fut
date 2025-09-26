#!/usr/bin/env python3
"""
Interface CLI principal para o Simulador de Futebol FIFA 25
Sistema interativo de linha de comando com menus e opções avançadas
"""
import sys
import os
import json
import argparse
import time
from pathlib import Path

# Adicionar src ao path
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))

# Adicionar config ao path
config_path = src_path.parent / "config"
sys.path.insert(0, str(config_path))

try:
    import config
except ImportError:
    print("[ERROR] Não foi possível carregar configurações. Verifique o arquivo config/config.yaml")
    sys.exit(1)


class FootballSimulatorCLI:
    """Interface CLI principal para simulação de futebol"""
    
    def __init__(self):
        self.config = config.config
        self.available_leagues = self.config.get("available_leagues", [
            "premier_league", "la_liga", "serie_a", "bundesliga", "ligue_1"
        ])
        self.current_league = self.config.get("league", "premier_league")
        
    def show_banner(self):
        """Exibe banner inicial do sistema"""
        print("=" * 80)
        print("                ⚽ SIMULADOR DE FUTEBOL FIFA 25 ⚽")
        print("                    Sistema de Linha de Comando")
        print("=" * 80)
        print(f"Liga atual: {self.current_league.replace('_', ' ').title()}")
        print(f"Ligas disponíveis: {len(self.available_leagues)}")
        print("-" * 80)
        
    def show_main_menu(self):
        """Exibe menu principal"""
        print("\n[MENU PRINCIPAL]")
        print("1. Executar Simulação")
        print("2. Configurar Liga")
        print("3. Ver Resultados Anteriores")
        print("4. Configurações do Sistema")
        print("5. Informações do Sistema")
        print("0. Sair")
        print("-" * 40)
        
    def show_simulation_menu(self):
        """Menu de tipos de simulação"""
        print("\n[TIPOS DE SIMULAÇÃO]")
        print("1. Simulação Simples (Rápida)")
        print("2. Simulação Avançada (Completa)")
        print("3. Simulação Personalizada")
        print("0. Voltar")
        print("-" * 40)
        
    def show_league_menu(self):
        """Menu de seleção de liga"""
        print("\n[SELEÇÃO DE LIGA]")
        for i, league in enumerate(self.available_leagues, 1):
            marker = " [ATUAL]" if league == self.current_league else ""
            print(f"{i}. {league.replace('_', ' ').title()}{marker}")
        print("0. Voltar")
        print("-" * 40)
        
    def get_user_choice(self, max_option):
        """Obtém escolha do usuário com validação"""
        while True:
            try:
                choice = input(f"\nEscolha uma opção (0-{max_option}): ").strip()
                if not choice:
                    continue
                    
                choice = int(choice)
                if 0 <= choice <= max_option:
                    return choice
                else:
                    print(f"[ERROR] Escolha deve ser entre 0 e {max_option}")
            except ValueError:
                print("[ERROR] Digite apenas números")
            except KeyboardInterrupt:
                print("\n[INFO] Operação cancelada pelo usuário")
                return 0
                
    def run_simple_simulation(self, league=None):
        """Executa simulação simples"""
        target_league = league or self.current_league
        
        print(f"\n[SIMULAÇÃO SIMPLES]")
        print(f"Liga: {target_league.replace('_', ' ').title()}")
        print("Iniciando simulação...")
        print("-" * 40)
        
        try:
            # Importar e executar simulador simples
            sys.path.insert(0, str(src_path / "core" / "simple"))
            import simulator
            
            # Executar com liga específica
            simulator.main(target_league)
            
            print("\n[SUCCESS] Simulação simples concluída!")
            
        except Exception as e:
            print(f"[ERROR] Erro na simulação simples: {e}")
            
    def run_advanced_simulation(self, league=None):
        """Executa simulação avançada"""
        target_league = league or self.current_league
        
        print(f"\n[SIMULAÇÃO AVANÇADA]")
        print(f"Liga: {target_league.replace('_', ' ').title()}")
        print("Iniciando simulação completa com estatísticas de jogadores...")
        print("-" * 40)
        
        try:
            import subprocess
            
            # Executar script de temporada completa
            script_path = src_path.parent / "scripts" / "run_season_simulation.py"
            
            result = subprocess.run([
                sys.executable, str(script_path), 
                "--league", target_league
            ], cwd=str(src_path.parent))
            
            if result.returncode == 0:
                print("\n[SUCCESS] Simulação avançada concluída!")
            else:
                print(f"[ERROR] Simulação falhou com código {result.returncode}")
            
        except Exception as e:
            print(f"[ERROR] Erro na simulação avançada: {e}")
            
    def run_custom_simulation(self):
        """Menu de simulação personalizada"""
        print("\n[SIMULAÇÃO PERSONALIZADA]")
        print("Escolha as opções de simulação:")
        print("-" * 40)
        
        # Escolher liga
        self.show_league_menu()
        league_choice = self.get_user_choice(len(self.available_leagues))
        
        if league_choice == 0:
            return
            
        selected_league = self.available_leagues[league_choice - 1]
        
        # Escolher tipo
        print(f"\nLiga selecionada: {selected_league.replace('_', ' ').title()}")
        print("\nTipo de simulação:")
        print("1. Simples")
        print("2. Avançada")
        print("0. Cancelar")
        
        sim_type = self.get_user_choice(2)
        
        if sim_type == 0:
            return
        elif sim_type == 1:
            self.run_simple_simulation(selected_league)
        else:
            self.run_advanced_simulation(selected_league)
            
    def configure_league(self):
        """Configura liga padrão"""
        print("\n[CONFIGURAÇÃO DE LIGA]")
        print("Liga atual:", self.current_league.replace('_', ' ').title())
        print("\nEscolha nova liga padrão:")
        
        self.show_league_menu()
        choice = self.get_user_choice(len(self.available_leagues))
        
        if choice == 0:
            return
            
        new_league = self.available_leagues[choice - 1]
        
        if new_league != self.current_league:
            self.current_league = new_league
            print(f"\n[SUCCESS] Liga alterada para: {new_league.replace('_', ' ').title()}")
            
            # Atualizar config (apenas em memória para esta sessão)
            print("[INFO] Alteração válida apenas para esta sessão")
            print("Para alteração permanente, edite config/config.yaml")
        else:
            print("\n[INFO] Liga mantida inalterada")
            
        input("\nPressione Enter para continuar...")
        
    def view_recent_results(self):
        """Visualiza resultados recentes"""
        print("\n[RESULTADOS ANTERIORES]")
        print("Liga atual:", self.current_league.replace('_', ' ').title())
        print("-" * 40)
        
        try:
            # Buscar resultados na pasta
            results_path = Path(self.config["paths"]["results"]) / self.current_league
            
            if not results_path.exists():
                print("[INFO] Nenhum resultado encontrado para esta liga")
                input("\nPressione Enter para continuar...")
                return
                
            # Buscar arquivos JSON (mais informativos)
            json_files = sorted(results_path.glob("*.json"), reverse=True)
            
            if not json_files:
                print("[INFO] Nenhum resultado em formato JSON encontrado")
                input("\nPressione Enter para continuar...")
                return
                
            print(f"Encontrados {len(json_files)} resultados:\n")
            
            # Mostrar últimos 10 resultados
            for i, file in enumerate(json_files[:10], 1):
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        
                    created_at = data.get("created_at", "Data não disponível")
                    simulation_type = data.get("simulation_type", "simples")
                    
                    # Tentar extrair campeão
                    champion = "N/A"
                    if "tabela_final" in data and data["tabela_final"]:
                        champion = data["tabela_final"][0].get("index", 
                                   list(data["tabela_final"][0].keys())[0])
                    
                    print(f"{i:2}. {file.name}")
                    print(f"    Criado em: {created_at}")
                    print(f"    Tipo: {simulation_type.title()}")
                    print(f"    Campeão: {champion}")
                    print()
                    
                except Exception as e:
                    print(f"{i:2}. {file.name} [ERRO: {e}]")
                    
            # Opção de ver detalhes
            print("\nOpções:")
            print("1. Ver detalhes de um resultado")
            print("2. Limpar resultados antigos")
            print("0. Voltar")
            
            choice = self.get_user_choice(2)
            
            if choice == 1:
                self.view_result_details(json_files[:10])
            elif choice == 2:
                self.clean_old_results(results_path)
                
        except Exception as e:
            print(f"[ERROR] Erro ao buscar resultados: {e}")
            input("\nPressione Enter para continuar...")
            
    def view_result_details(self, files):
        """Mostra detalhes de um resultado específico"""
        print(f"\nEscolha o resultado para ver detalhes (1-{len(files)}):")
        choice = self.get_user_choice(len(files))
        
        if choice == 0:
            return
            
        selected_file = files[choice - 1]
        
        try:
            with open(selected_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            print(f"\n[DETALHES] {selected_file.name}")
            print("=" * 60)
            
            # Informações gerais
            print(f"Data: {data.get('created_at', 'N/A')}")
            print(f"Tipo: {data.get('simulation_type', 'simples').title()}")
            print(f"Liga: {data.get('league', self.current_league).replace('_', ' ').title()}")
            print(f"Versão: {data.get('version', 'N/A')}")
            print()
            
            # Tabela final (primeiros 10)
            if "tabela_final" in data and data["tabela_final"]:
                print("TABELA FINAL (Top 10):")
                print("-" * 40)
                
                for i, team_data in enumerate(data["tabela_final"][:10], 1):
                    if isinstance(team_data, dict):
                        # Tentar extrair nome do time de diferentes formas
                        team_name = (team_data.get("index") or 
                                   team_data.get("team") or 
                                   team_data.get("Time") or
                                   list(team_data.keys())[0])
                        
                        points = team_data.get("P", team_data.get("points", "N/A"))
                        
                        print(f"{i:2}º {team_name:<25} {points:>3} pts")
                        
            print()
            
        except Exception as e:
            print(f"[ERROR] Erro ao ler arquivo: {e}")
            
        input("\nPressione Enter para continuar...")
        
    def clean_old_results(self, results_path):
        """Opção para limpar resultados antigos"""
        print("\n[LIMPEZA DE RESULTADOS]")
        print(f"Pasta: {results_path}")
        
        files = list(results_path.glob("*"))
        print(f"Total de arquivos: {len(files)}")
        
        if len(files) == 0:
            print("[INFO] Pasta já está vazia")
            input("\nPressione Enter para continuar...")
            return
            
        print("\nOpções:")
        print("1. Manter apenas os 5 mais recentes")
        print("2. Manter apenas os 10 mais recentes")
        print("3. Limpar tudo")
        print("0. Cancelar")
        
        choice = self.get_user_choice(3)
        
        if choice == 0:
            return
            
        try:
            if choice == 3:
                # Limpar tudo
                for file in files:
                    file.unlink()
                print(f"[SUCCESS] {len(files)} arquivos removidos")
            else:
                # Manter apenas N mais recentes
                keep_count = 5 if choice == 1 else 10
                
                # Ordenar por data de modificação
                sorted_files = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
                
                if len(sorted_files) <= keep_count:
                    print(f"[INFO] Apenas {len(sorted_files)} arquivos encontrados, mantendo todos")
                else:
                    files_to_remove = sorted_files[keep_count:]
                    for file in files_to_remove:
                        file.unlink()
                    print(f"[SUCCESS] {len(files_to_remove)} arquivos antigos removidos")
                    print(f"Mantidos os {keep_count} mais recentes")
                    
        except Exception as e:
            print(f"[ERROR] Erro na limpeza: {e}")
            
        input("\nPressione Enter para continuar...")
        
    def show_system_settings(self):
        """Mostra configurações do sistema"""
        print("\n[CONFIGURAÇÕES DO SISTEMA]")
        print("=" * 50)
        
        print(f"Liga padrão: {self.current_league.replace('_', ' ').title()}")
        print(f"Ligas disponíveis: {', '.join([l.replace('_', ' ').title() for l in self.available_leagues])}")
        print()
        
        # Configurações de simulação
        sim_config = self.config.get("simulation", {})
        print("SIMULAÇÃO:")
        print(f"  Turno duplo: {sim_config.get('double_round', 'N/A')}")
        print(f"  Seed: {sim_config.get('seed', 'Aleatório')}")
        print(f"  Fator aleatório: {sim_config.get('random_factor_min', 'N/A')} - {sim_config.get('random_factor_max', 'N/A')}")
        print()
        
        # Caminhos
        paths = self.config.get("paths", {})
        print("CAMINHOS:")
        for key, value in paths.items():
            print(f"  {key}: {value}")
        print()
        
        # Configurações de saída
        output = self.config.get("output", {})
        print("SAÍDA:")
        for key, value in output.items():
            print(f"  {key}: {value}")
            
        input("\nPressione Enter para continuar...")
        
    def show_system_info(self):
        """Mostra informações do sistema"""
        print("\n[INFORMAÇÕES DO SISTEMA]")
        print("=" * 50)
        
        print("SIMULADOR DE FUTEBOL FIFA 25")
        print("Versão: 2.0.0")
        print("Autor: Vini Ruggeri")
        print()
        
        print("FUNCIONALIDADES:")
        print("- Simulação simples (estatística)")
        print("- Simulação avançada (jogadores)")
        print("- 5 ligas europeias suportadas")
        print("- Interface CLI e Web")
        print("- Suporte Docker")
        print("- Dados reais FIFA 25")
        print()
        
        print("LIGAS SUPORTADAS:")
        for league in self.available_leagues:
            print(f"- {league.replace('_', ' ').title()}")
        print()
        
        print("REQUISITOS:")
        print("- Python 3.11+")
        print("- pandas, numpy, pyyaml")
        print("- streamlit (para interface web)")
        print()
        
        # Verificar existência de dados
        try:
            data_path = Path(self.config["paths"]["json_ligas"])
            if data_path.exists():
                json_files = list(data_path.glob("*.json"))
                print(f"DADOS: {len(json_files)} arquivos de liga encontrados")
            else:
                print("DADOS: Pasta de dados não encontrada")
        except:
            print("DADOS: Erro ao verificar dados")
            
        input("\nPressione Enter para continuar...")
        
    def run_interactive_mode(self):
        """Executa modo interativo principal"""
        while True:
            try:
                self.show_banner()
                self.show_main_menu()
                
                choice = self.get_user_choice(5)
                
                if choice == 0:
                    print("\n[INFO] Encerrando simulador...")
                    print("Obrigado por usar o Simulador de Futebol FIFA 25!")
                    break
                    
                elif choice == 1:
                    # Menu de simulação
                    while True:
                        self.show_simulation_menu()
                        sim_choice = self.get_user_choice(3)
                        
                        if sim_choice == 0:
                            break
                        elif sim_choice == 1:
                            self.run_simple_simulation()
                        elif sim_choice == 2:
                            self.run_advanced_simulation()
                        elif sim_choice == 3:
                            self.run_custom_simulation()
                            
                elif choice == 2:
                    self.configure_league()
                elif choice == 3:
                    self.view_recent_results()
                elif choice == 4:
                    self.show_system_settings()
                elif choice == 5:
                    self.show_system_info()
                    
            except KeyboardInterrupt:
                print("\n\n[INFO] Encerrando por solicitação do usuário...")
                break
            except Exception as e:
                print(f"\n[ERROR] Erro inesperado: {e}")
                input("\nPressione Enter para continuar...")


def main():
    """Função principal da CLI"""
    parser = argparse.ArgumentParser(
        description="Simulador de Futebol FIFA 25 - Interface CLI",
        epilog="Exemplos: python cli.py --interactive | python cli.py --quick --league premier_league"
    )
    
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Modo interativo com menus")
    parser.add_argument("--quick", "-q", action="store_true",
                       help="Simulação rápida sem menus")
    parser.add_argument("--league", "-l", type=str,
                       help="Liga para simulação (premier_league, la_liga, etc.)")
    parser.add_argument("--type", "-t", choices=["simple", "advanced"], default="simple",
                       help="Tipo de simulação (simple ou advanced)")
    parser.add_argument("--list-leagues", action="store_true",
                       help="Lista ligas disponíveis e sai")
    
    args = parser.parse_args()
    
    cli = FootballSimulatorCLI()
    
    # Modo lista ligas
    if args.list_leagues:
        print("Ligas disponíveis:")
        for i, league in enumerate(cli.available_leagues, 1):
            marker = " [PADRÃO]" if league == cli.current_league else ""
            print(f"  {i}. {league}{marker}")
        return 0
    
    # Modo rápido
    if args.quick:
        league = args.league or cli.current_league
        
        print(f"[MODO RÁPIDO] {args.type.upper()} - {league.replace('_', ' ').title()}")
        
        if args.type == "simple":
            cli.run_simple_simulation(league)
        else:
            cli.run_advanced_simulation(league)
            
        return 0
    
    # Modo interativo (padrão)
    cli.run_interactive_mode()
    return 0


if __name__ == "__main__":
    sys.exit(main())