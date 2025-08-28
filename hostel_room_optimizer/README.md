
# Hostel Room Allocation Optimizer

An end-to-end, free-to-run AI/ML project that optimizes roommate assignments using clustering.
This project is written in Python and includes a Streamlit demo app, synthetic data generator,
and a simple clustering-based allocation model (K-Means).

## Features
- Generate synthetic student preference data
- Cluster students by compatibility (sleep schedule, study habit, cleanliness, smoking, hometown)
- Allocate students into rooms with a configurable room capacity
- Streamlit app for interactive demo (upload CSV or generate synthetic data)
- Free tech stack: Python, scikit-learn, pandas, Streamlit

## Files
- `app.py` - Streamlit web app to run the demo
- `generate_data.py` - Script to create synthetic student data (CSV)
- `model.py` - Clustering & allocation logic used by the app
- `sample_data.csv` - Example synthetic dataset
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Quickstart (local)
1. Create and activate a Python virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Open the link shown by Streamlit (usually http://localhost:8501).

## How it works (short)
1. Each student has numeric features representing preferences (sleep_time, study_pref, cleanliness, smoking, hometown_group).
2. K-Means groups similar students; labels are used to form roommate groups.
3. A greedy packing step distributes cluster members into rooms of fixed capacity to balance loads.

## Notes & Extensions
- Replace K-Means with constrained clustering or optimization (Hungarian algorithm) for stricter constraints.
- Extend with survey forms, anonymized real data, or roommate satisfaction feedback loop.
- Add persistence (Postgres) and deployment (Streamlit Cloud / Render).

