@echo off
REM Interface CLI do Simulador de Futebol FIFA 25
REM Uso: cli.bat [argumentos]
REM Exemplos:
REM   cli.bat                          - Modo interativo
REM   cli.bat --quick                  - Simulacao rapida
REM   cli.bat --league premier_league  - Liga especifica

echo Simulador de Futebol FIFA 25 - Interface CLI
echo.

cd /d %~dp0
python cli.py %*

if errorlevel 1 (
    echo.
    echo [ERROR] Erro na execucao. Verifique se Python e dependencias estao instalados.
    echo Use: pip install -r requirements.txt
    pause
)