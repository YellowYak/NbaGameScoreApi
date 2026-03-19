import json
import re
from dataclasses import asdict
from datetime import date, datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from nba_watchability import score_date, score_game
from nba_watchability.exceptions import NbaWatchabilityError

app = FastAPI(title="NBA Game Score API")

_DATE_RE = re.compile(r"^\d{8}$")


def _json_default(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/score/game")
def get_score_game(url: str):
    try:
        result = score_game(url)
    except NbaWatchabilityError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    payload = json.loads(
        json.dumps(asdict(result), default=_json_default)
    )
    return JSONResponse(content=payload)


@app.get("/score/{date_str}")
def get_score(date_str: str):
    if not _DATE_RE.match(date_str):
        raise HTTPException(status_code=400, detail="Date must be 8 digits in YYYYMMDD format")

    try:
        datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date value")

    try:
        results = score_date(date_str)
    except NbaWatchabilityError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    payload = json.loads(
        json.dumps([asdict(r) for r in results], default=_json_default)
    )
    return JSONResponse(content=payload)
