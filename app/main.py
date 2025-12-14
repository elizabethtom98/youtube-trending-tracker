from typing import List

from fastapi import FastAPI, Query
from pydantic import BaseModel

from app.yt_service import fetch_trending, normalize_items
from app.mongo_service import upsert_many, ensure_indexes

app = FastAPI(title="YT Trending Tracker")

# Default regions to load in batch (you can change this list)
DEFAULT_REGIONS = ["AU", "IN", "US", "CA", "GB"]


@app.on_event("startup")
def startup():
    # Make sure indexes exist when the app starts
    ensure_indexes()


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "YT Trending Tracker API running. See /docs for interactive UI.",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Models ----------

class JobResult(BaseModel):
    region: str
    capturedAt: str
    fetched: int
    upserted: int


class BatchJobResult(BaseModel):
    jobs: List[JobResult]


# ---------- Single-region job ----------

@app.post("/jobs/fetch-trending", response_model=JobResult)
def run_job(
    region: str = Query("AU", description="Two-letter region code like AU, IN, US, CA, GB"),
    max_results: int = Query(20, ge=1, le=50),
):
    """
    Fetch trending videos for a single region and store them in MongoDB.
    """
    payload = fetch_trending(region=region, max_results=max_results)
    rows = normalize_items(payload)
    result = upsert_many(rows)

    return JobResult(
        region=region,
        capturedAt=payload["_captured_at"],
        fetched=len(rows),
        upserted=result.get("upserted", 0),
    )


# ---------- Multi-region job ----------

@app.post("/jobs/fetch-multi", response_model=BatchJobResult)
def run_multi_job(
    regions: List[str] = Query(
        DEFAULT_REGIONS,
        description="List of region codes. If omitted, defaults to AU, IN, US, CA, GB.",
    ),
    max_results: int = Query(50, ge=1, le=50),
):
    """
    Fetch trending videos for multiple regions in one call and store them in MongoDB.
    """
    jobs: List[JobResult] = []

    for region in regions:
        payload = fetch_trending(region=region, max_results=max_results)
        rows = normalize_items(payload)
        result = upsert_many(rows)

        jobs.append(
            JobResult(
                region=region,
                capturedAt=payload["_captured_at"],
                fetched=len(rows),
                upserted=result.get("upserted", 0),
            )
        )

    return BatchJobResult(jobs=jobs)
