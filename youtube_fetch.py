from app.yt_service import fetch_trending, normalize_items
from app.mongo_service import upsert_many, ensure_indexes

# Ensure indexes
ensure_indexes()

# Fetch trending videos
payload = fetch_trending(region="AU", max_results=5)
rows = normalize_items(payload)

# Save to Mongo
result = upsert_many(rows)
print("Mongo Result:", result)
