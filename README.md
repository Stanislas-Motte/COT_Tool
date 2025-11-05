# Commodities COT Data Analysis

This project loads and visualizes Commitments of Traders (COT) futures data from the CFTC.

## Setup

1. Create and activate virtual environment:
```bash
./setup_env.sh
# or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Register Jupyter kernel:
```bash
python -m ipykernel install --user --name=commodities --display-name="Python (commodities)"
```

## Usage

### 1. Load Data into Database

**Option A: Using the notebook**
- Open `explore_data.ipynb`
- Run all cells to load, filter, and export data to SQLite

**Option B: Using the script**
```bash
python load_to_database.py
```

This creates `commodities.db` with the filtered COT data.

### 2. Run Visualization App

```bash
streamlit run app.py
```

The app will open in your browser where you can:
- Select any commodity from the dropdown
- Choose date ranges
- Visualize multiple columns with interactive charts
- View summary statistics and raw data
- Export filtered data as CSV

## Files

- `explore_data.ipynb` - Jupyter notebook for data exploration and filtering
- `load_to_database.py` - Script to load Excel files into SQLite database
- `app.py` - Streamlit web app for visualization
- `commodities.db` - SQLite database (created after running load script)
- `requirements.txt` - Python dependencies
