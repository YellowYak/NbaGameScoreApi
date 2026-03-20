# NBA Game Score API

A thin FastAPI wrapper around the [nba-watchability](https://github.com/YellowYak/NbaGameScore) library.

## Install and run locally

**Prerequisites:** Python 3.11+

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Install the project and its dependencies
pip install -e .

# 3. Start the development server
uvicorn api.main:app --reload
```

The API will be available at http://localhost:8000.

## Run with Docker

```bash
# Build the image
docker build -t nba-game-score-api .

# Run the container (exposes the API on port 8000)
docker run -p 8000:8000 --name nba-api nba-game-score-api
```

The API will be available at http://localhost:8000.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/score/{YYYYMMDD}` | Watchability scores for all games on a date |
| GET | `/score/game?url={bbref_url}` | Watchability score for a single game by basketball-reference.com boxscore URL |

### Examples

```bash
curl http://localhost:8000/score/20250101
curl "http://localhost:8000/score/game?url=https://www.basketball-reference.com/boxscores/202503140DEN.html"
```
