# Setup (lokal utvikling)
-Denne guiden beskriver hvordan prosjektet kjøres lokalt på utviklingsmaskin (macOS, Windows eller Linux). Deployment til server er beskrevet i deployment.md.


## Krav
- Docker Desktop
- Git
- VS Code (anbefalt)

## klone repo
- git clone https://github.com/KristianTalgo/wombo
- cd wombo

## starte serveren
- docker compose up --build

## åpne app
- http://localhost:8000

## ved deployment på VM:
- http://<VM-IP>:8000

## stoppe siden
- docker compose down

## kjøre db-migrasjoner
- kjøres automatisk med docker compose up --build

## forced instalasjon av requirements-pakker
- docker compose build --no-cache



