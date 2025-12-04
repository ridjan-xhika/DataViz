from src.data_fetch import load_confirmed, load_deaths, load_recovered
from src.database import DatabaseConnection, init_database
import pandas as pd
from datetime import datetime

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except:
        return None

def sync_covid_data():
    print("Initializing database...")
    init_database()
    
    print("Loading COVID-19 data from GitHub...")
    df_confirmed = load_confirmed()
    df_deaths = load_deaths()
    df_recovered = load_recovered()
    
    db = DatabaseConnection()
    db.connect()
    
    print("Processing and inserting data into MySQL...")
    
    cursor = db.connection.cursor()
    
    date_columns = df_confirmed.columns[4:]
    
    for idx, row in df_confirmed.iterrows():
        country = row['Country/Region']
        province = row['Province/State'] if pd.notna(row['Province/State']) else None
        latitude = row['Lat'] if pd.notna(row['Lat']) else None
        longitude = row['Long'] if pd.notna(row['Long']) else None
        
        for date_col in date_columns:
            parsed_date = parse_date(date_col)
            if not parsed_date:
                continue
                
            confirmed = int(row[date_col]) if pd.notna(row[date_col]) else 0
            
            deaths_idx = (df_deaths['Country/Region'] == country) & (df_deaths['Province/State'] == province if pd.notna(province) else df_deaths['Province/State'].isna())
            deaths_val = int(df_deaths.loc[deaths_idx, date_col].values[0]) if len(df_deaths.loc[deaths_idx, date_col].values) > 0 else 0
            
            recovered_idx = (df_recovered['Country/Region'] == country) & (df_recovered['Province/State'] == province if pd.notna(province) else df_recovered['Province/State'].isna())
            recovered_val = int(df_recovered.loc[recovered_idx, date_col].values[0]) if len(df_recovered.loc[recovered_idx, date_col].values) > 0 else 0
            
            query = """
                INSERT INTO covid_data (country, province, latitude, longitude, date, confirmed, deaths, recovered)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            try:
                cursor.execute(query, (country, province, latitude, longitude, parsed_date, confirmed, deaths_val, recovered_val))
            except Exception as e:
                pass
        
        if (idx + 1) % 50 == 0:
            print(f"Processed {idx + 1} regions...")
    
    db.connection.commit()
    cursor.close()
    db.disconnect()
    
    print("Data sync complete!")

if __name__ == "__main__":
    sync_covid_data()
