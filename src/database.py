import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict

class DatabaseConnection:
    def __init__(self, host: str = "localhost", user: str = "root", password: str = "root", database: str = "covid19"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection
        except Error as e:
            print(f"Error: {e}")
            return None
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
        except Error as e:
            print(f"Query error: {e}")
            return None
        finally:
            cursor.close()
    
    def insert_data(self, table: str, columns: List[str], values: List[tuple]):
        placeholders = ', '.join(['%s'] * len(columns))
        col_names = ', '.join(columns)
        query = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
        
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, values)
            self.connection.commit()
            print(f"Inserted {cursor.rowcount} rows")
        except Error as e:
            print(f"Insert error: {e}")
        finally:
            cursor.close()

def init_database():
    db = DatabaseConnection()
    if not db.connect():
        print("Failed to connect to MySQL database")
        return False
    
    cursor = db.connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS covid_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country VARCHAR(255),
            province VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT,
            date DATE,
            confirmed INT,
            deaths INT,
            recovered INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    db.connection.commit()
    cursor.close()
    db.disconnect()
    return True
