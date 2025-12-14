import os
from datetime import date

import certifi
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient

# ---------------- Env + setup ----------------
load_dotenv()

st.set_page_config(page_title="YouTube Trending Dashboard", layout="wide")
st.title("📈 YouTube Trending Tracker")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "yt_tracker")

if not MONGO_URI:
    st.error("MONGO_URI missing. Add it to your .env or export before running.")
    st.stop()

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000,
)
db = client[MONGO_DB]
coll = db["videos"]

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filters")

# Regions
try:
    regions = sorted(
        list(
            {d["regionCode"] for d in coll.find({}, {"regionCode": 1, "_id": 0}).limit(500)}
        )
    )
except Exception:
    regions = ["AU", "US", "IN", "GB", "CA"]

region = st.sidebar.selectbox("Region", options=regions or ["AU"], index=0)

# Date (captured date)
picked_date = st.sidebar.date_input("Captured date", value=date.today())
date_prefix = picked_date.isoformat()

# Limit rows
limit = st.sidebar.slider("Max rows", 100, 2000, 500, step=100)

# ---------------- Query Mongo ----------------
query = {"regionCode": region, "capturedAt": {"$regex": f"^{date_prefix}"}}
fields = {
    "_id": 0,
    "videoId": 1,
    "title": 1,
    "channelId": 1,
    "channelTitle": 1,
    "categoryId": 1,
    "publishedAt": 1,
    "views": 1,
    "likes": 1,
    "comments": 1,
    "regionCode": 1,
    "capturedAt": 1,
}

docs = list(coll.find(query, fields).limit(limit))
df = pd.DataFrame(docs)

if df.empty:
    st.info(
        "No data for the chosen filters. Run your ETL job for this region/date, or pick another date."
    )
    st.stop()

# ---------------- "Last Updated" timestamp ----------------
latest_ts = df["capturedAt"].max()
st.caption(f"**Data last updated:** {latest_ts} UTC")

# ---------------- Enrich & clean data ----------------
for col in ["views", "likes", "comments"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["engagement_rate"] = (df["likes"] + df["comments"]) / df["views"].replace(0, np.nan)
df["engagement_rate"] = df["engagement_rate"].fillna(0)

CATEGORY_MAP = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "17": "Sports",
    "20": "Gaming",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "How-to & Style",
    "27": "Education",
    "28": "Science & Tech",
}
df["category"] = df["categoryId"].astype(str).map(CATEGORY_MAP).fillna("Other")

# ---------------- Channel Filter ----------------
channels = sorted(df["channelTitle"].unique())
selected_channel = st.sidebar.selectbox("Filter by Channel (optional)", ["All"] + channels)

if selected_channel != "All":
    df = df[df["channelTitle"] == selected_channel]

# ---------------- KPIs ----------------
total_views = int(df["views"].sum())
avg_engagement = df["engagement_rate"].mean() * 100

top_video = df.sort_values("views", ascending=False).iloc[0]
top_video_title = top_video["title"]
if len(top_video_title) > 40:
    top_video_title = top_video_title[:37] + "..."

top_category = (
    df.groupby("category")["views"].sum().sort_values(ascending=False).index[0]
)
top_channel = (
    df.groupby("channelTitle")["views"].sum().sort_values(ascending=False).index[0]
)

st.markdown("### Overview")

c1, c2, c3 = st.columns(3)
c4, c5 = st.columns(2)

c1.metric("Top Video (by views)", top_video_title)
c2.metric("Top Channel (by views)", top_channel)
c3.metric("Top Category (by views)", top_category)

c4.metric("Total Views (approx)", f"{total_views:,.0f}")
c5.metric("Avg Engagement Rate", f"{avg_engagement:,.1f}%")

st.markdown("---")

# ---------------- Add Thumbnails + Watch Links ----------------
df["thumbnail"] = df["videoId"].apply(
    lambda vid: f"https://img.youtube.com/vi/{vid}/0.jpg"
)
df["url"] = df["videoId"].apply(
    lambda vid: f"https://youtube.com/watch?v={vid}"
)

# ---------------- Top 10 videos table ----------------
st.markdown("### Top 10 Trending Videos ")

top_videos = (
    df.sort_values("views", ascending=False)
    .head(10)[
        ["thumbnail", "title", "channelTitle", "category",
         "views", "likes", "comments", "url"]
    ]
    .rename(
        columns={
            "thumbnail": "Thumbnail",
            "title": "Title",
            "channelTitle": "Channel",
            "category": "Category",
            "views": "Views",
            "likes": "Likes",
            "comments": "Comments",
            "url": "Watch",
        }
    )
).reset_index(drop=True)

st.dataframe(
    top_videos,
    use_container_width=True,
    column_config={
        "Thumbnail": st.column_config.ImageColumn(
            "Thumbnail", help="Video thumbnail", width="large"
        ),
        "Watch": st.column_config.LinkColumn(
            "Watch", help="Open on YouTube", display_text="▶ Open"
        ),
    },
)


# ---------------- Charts ----------------
st.markdown("### Top Categories by Total Views")
cat_views = (
    df.groupby("category")["views"]
    .sum()
    .sort_values(ascending=False)
    .head(8)
    .reset_index()
)
st.bar_chart(cat_views, x="category", y="views")

st.markdown("### Top Channels by Total Views")
chan_views = (
    df.groupby("channelTitle")["views"]
    .sum()
    .sort_values(ascending=False)
    .head(8)
    .reset_index()
)
st.bar_chart(chan_views, x="channelTitle", y="views")
