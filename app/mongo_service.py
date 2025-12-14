import os
from pymongo import MongoClient, UpdateOne
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "yt_tracker")

# Create connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collection
videos = db["videos"]


def ensure_indexes():
    """Create useful indexes for performance + dedup."""
    videos.create_index("docKey", unique=True)
    videos.create_index([("regionCode", 1), ("capturedAt", 1)])
    videos.create_index("channelId")


def upsert_many(rows):
    """Insert OR update documents — avoids duplicates."""
    ops = []
    for r in rows:
        # Create docKey to prevent duplicates
        r["docKey"] = f"{r['videoId']}::{r['capturedAt'][:10]}::{r['regionCode']}"

        ops.append(
            UpdateOne({"docKey": r["docKey"]}, {"$set": r}, upsert=True)
        )

    if not ops:
        return {"status": "no-op"}

    result = videos.bulk_write(ops, ordered=False)

    return {
        "matched": result.matched_count,
        "modified": result.modified_count,
        "upserted": len(result.upserted_ids),
    }
