#!/bin/bash
LEAGUE=${1:-premier_league}   # default premier_league
docker build -t advanced_sim .
docker run --rm -e LEAGUE=$LEAGUE -v $(pwd)/results:/app/results advanced_sim
