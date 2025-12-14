# 📈 YouTube Trending Tracker

An end-to-end **data engineering + analytics** project that ingests YouTube trending video data via API, stores historical snapshots in MongoDB, and visualizes insights through an interactive Streamlit dashboard.

---

## 🚀 Project Overview

The **YouTube Trending Tracker** collects trending video data from multiple countries, processes and stores it in a database, and surfaces insights such as:

- Top trending videos
- Top channels and categories
- Engagement rate (likes + comments vs views)
- Regional snapshots by date

Unlike static CSV dashboards, this simulates a **production-style pipeline**: API → ETL service → database → dashboard.

---

## 🧱 Architecture

