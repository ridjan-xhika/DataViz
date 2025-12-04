import os
from pathlib import Path
import requests
import pandas as pd

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master"
DATA_DIR = Path(__file__).parent.parent / "data"

TIME_SERIES_CONFIRMED = (
    f"{GITHUB_RAW_BASE}/csse_covid_19_data/csse_covid_19_time_series/"
    "time_series_covid19_confirmed_global.csv"
)
TIME_SERIES_DEATHS = (
    f"{GITHUB_RAW_BASE}/csse_covid_19_data/csse_covid_19_time_series/"
    "time_series_covid19_deaths_global.csv"
)
TIME_SERIES_RECOVERED = (
    f"{GITHUB_RAW_BASE}/csse_covid_19_data/csse_covid_19_time_series/"
    "time_series_covid19_recovered_global.csv"
)


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_csv(url: str, filename: str, force_refresh: bool = False) -> pd.DataFrame:
    ensure_data_dir()
    filepath = DATA_DIR / filename
    
    if filepath.exists() and not force_refresh:
        print(f"Loading {filename} from cache...")
        return pd.read_csv(filepath)
    
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        filepath.write_text(response.text)
        print(f"Saved to {filepath}")
        return pd.read_csv(filepath)
    except requests.RequestException as e:
        print(f"Error fetching {filename}: {e}")
        raise


def load_confirmed(force_refresh: bool = False) -> pd.DataFrame:
    return fetch_csv(TIME_SERIES_CONFIRMED, "confirmed.csv", force_refresh)


def load_deaths(force_refresh: bool = False) -> pd.DataFrame:
    return fetch_csv(TIME_SERIES_DEATHS, "deaths.csv", force_refresh)


def load_recovered(force_refresh: bool = False) -> pd.DataFrame:
    return fetch_csv(TIME_SERIES_RECOVERED, "recovered.csv", force_refresh)


def print_data_summary():
    print("\n" + "="*60)
    print("COVID-19 Data Summary")
    print("="*60)
    
    try:
        df = load_confirmed()
        print(f"\nConfirmed Cases Dataset:")
        print(f"  Shape: {df.shape}")
        print(f"  Countries/Regions: {df['Country/Region'].nunique()}")
        print(f"  Date range: {df.columns[4]} to {df.columns[-1]}")
        print(f"\n  Latest totals (sample):")
        latest_col = df.columns[-1]
        print(f"    Global confirmed: {df[latest_col].sum():,.0f}")
        
        df_deaths = load_deaths()
        print(f"    Global deaths: {df_deaths[latest_col].sum():,.0f}")
        
        df_recovered = load_recovered()
        print(f"    Global recovered: {df_recovered[latest_col].sum():,.0f}")
        
    except Exception as e:
        print(f"Error loading data: {e}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    print_data_summary()
