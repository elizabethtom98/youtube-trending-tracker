**YouTube Trending Tracker**
An end-to-end data engineering and analytics project that ingests YouTube trending video data via API, stores historical snapshots in MongoDB, and visualizes actionable insights through an interactive Streamlit dashboard.
This project demonstrates real-world ETL design, API integration, data modelling, automation readiness, and analytics storytelling.
**Project Overview**
The YouTube Trending Tracker collects daily trending video data from multiple countries, processes and stores it in a cloud database, and exposes insights such as:
-Top trending videos
-Top channels and categories
-Engagement rates (likes + comments vs views)
-Regional and temporal trends
-Unlike static CSV-based dashboards, this project simulates a production-style data pipeline with automated ingestion, backend services, and a live analytics UI.
**Architecture**
-YouTube Data API
-       ↓
-FastAPI (ETL Service)
-       ↓
-MongoDB Atlas (Cloud Database)
-       ↓
-Streamlit Dashboard (Analytics & Visualization)
-Components:
-FastAPI – Backend service for data ingestion and ETL jobs
-MongoDB Atlas – Stores time-stamped trending snapshots
-Streamlit – Interactive analytics dashboard
-Scheduler Script – Designed for daily automation (cron / GitHub Actions ready)
**Data Pipeline (ETL Flow)**
**Extract**
-Fetches trending videos using the YouTube Data API
-Supports multiple regions (AU, US, IN, CA, GB, etc.)
**Transform**
-Normalizes nested JSON
-Converts metrics to numeric format
-Calculates engagement rates
-Maps category IDs to readable names
-Generates unique document keys to avoid duplicates
**Load**
-Upserts data into MongoDB

**📊 Dashboard Features**
**🔹 Overview KPIs**
-Top video by views
-Top channel by total views
-Top category by total views
-Total views (approx.)
-Average engagement rate
**🔹 Interactive Filters**
-Region selector
-Captured date selector
-Optional channel filter
**🔹 Visualizations**
-Top categories by total views
-Top channels by total views
-Top 10 trending videos table

**🔹 UX Enhancements**
-Thumbnail previews
-Click-to-watch links
-Clean tables 
-“Last updated” timestamp
**⚙️ Technologies Used**
Layer	Tools
Language	Python
Backend	FastAPI
Database	MongoDB Atlas
Dashboard	Streamlit
API	YouTube Data API
Data	Pandas, NumPy
Security	dotenv, certifi
Version Control	Git & GitHub
🕒 Automation & Scheduling
The project includes a scheduler script designed to trigger the ETL job automatically.
In a production environment, this scheduler can be executed via:
Cron jobs
GitHub Actions
Cloud schedulers (AWS EventBridge / GCP Cloud Scheduler)
For portfolio purposes, the automation logic is implemented and documented without requiring a continuously running server.
▶️ How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/youtube-trending-tracker.git
cd youtube-trending-tracker
2️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Configure environment variables
Create a .env file:
YOUTUBE_API_KEY=your_api_key
MONGO_URI=your_mongodb_uri
MONGO_DB=yt_tracker
5️⃣ Run ETL job (via API)
uvicorn app.main:app --reload
Trigger ingestion:
POST http://127.0.0.1:8000/jobs/fetch-trending?region=AU&max_results=50
6️⃣ Launch dashboard
streamlit run streamlit_app/dashboard.py
📌 Sample Use Cases
Media & entertainment trend analysis
Content performance benchmarking
Regional popularity comparison
Engagement pattern analysis
Data engineering portfolio demonstration
🎯 Key Skills Demonstrated
API integration & data ingestion
ETL pipeline design
Cloud database modelling
Data normalization & deduplication
Backend service development
Analytics dashboard design
Automation readiness
Clean, modular architecture
🔮 Future Enhancements
Global cross-region comparison charts
Time-series trend analysis
Deployment to cloud (AWS / GCP)
Authentication & role-based access
Category-level engagement benchmarking
👩‍💻 Author
Elizabeth Tom
Master of Computer Science – University of Wollongong
Data Engineering & Analytics Enthusiast
