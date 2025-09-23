@echo off
SET LEAGUE=%1
IF "%LEAGUE%"=="" SET LEAGUE=premier_league
docker build -t advanced_sim .
docker run --rm -e LEAGUE=%LEAGUE% -v %cd%\results:/app/results advanced_sim
pause
