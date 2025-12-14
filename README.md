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

YouTube Data API
↓
FastAPI (ETL Service)
↓
MongoDB Atlas (Database)
↓
Streamlit Dashboard (Analytics UI)

---

## 🔄 Data Pipeline (ETL)

1. **Extract**
   - Fetch trending videos from the YouTube Data API (`chart=mostPopular`)
   - Supports multiple regions (AU, IN, US, CA, GB, etc.)

2. **Transform**
   - Normalize nested JSON into a flat table-like structure
   - Convert metrics to numeric values
   - Compute engagement rate
   - Map category IDs to readable names

3. **Load**
   - Upsert into MongoDB (dedup using a unique document key)
   - Create indexes for fast filtering (region/date/channel)

---

## 📊 Dashboard Features

### Overview KPIs
- Top video (by views)
- Top channel (by total views)
- Top category (by total views)
- Total views (approx.)
- Average engagement rate

### Interactive filters
- Region
- Captured date
- Optional channel filter

### UX enhancements
- Video thumbnails
- Clickable YouTube links
- “Last updated” timestamp

---

## ⚙️ Tech Stack

- **Python**
- **FastAPI** (ETL service)
- **MongoDB Atlas** (database)
- **Streamlit** (dashboard)
- **Pandas / NumPy**
- **YouTube Data API**
- **dotenv / certifi**
- **Git & GitHub**

---

## 🕒 Automation (Scheduler-ready)

This project includes a scheduler script designed to trigger the ETL job automatically.

In a production setup, it can be scheduled using:
- cron
- GitHub Actions
- Cloud schedulers (AWS EventBridge / GCP Cloud Scheduler)

---

## ▶️ Run Locally

### 1) Clone
```bash
git clone https://github.com/YOUR_USERNAME/youtube-trending-tracker.git
cd youtube-trending-tracker
## ▶️ Run Locally

###** Create & activate virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
```

```bash
.venv\Scripts\activate      # Windows
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Create environment variables

Create a file named `.env` in the project root:

```env
YOUTUBE_API_KEY=your_api_key
MONGO_URI=your_mongodb_uri
MONGO_DB=yt_tracker
```

---

### Start the FastAPI ETL service

```bash
uvicorn app.main:app --reload
```

API documentation:

```
http://127.0.0.1:8000/docs
```

Trigger ETL jobs:

```
POST /jobs/fetch-trending?region=AU&max_results=50
POST /jobs/fetch-multi?regions=AU&regions=IN&regions=US&max_results=50
```

---

### Run the Streamlit dashboard

```bash
streamlit run streamlit_app/dashboard.py
```

---

## 🕒 Automation

The project includes a scheduler script designed for automated ingestion.

In production, this pipeline can be triggered using:
- cron
- GitHub Actions
- Cloud schedulers (AWS / GCP)

---

## 🎯 Skills Demonstrated

- API-based data ingestion
- ETL pipeline design
- Backend development with FastAPI
- Cloud database modelling (MongoDB Atlas)
- Interactive analytics dashboard development
- Automation-ready architecture

---

## 👩‍💻 Author

**Elizabeth Tom**  
Master of Computer Science – University of Wollongong  
Data Engineering & Analytics

