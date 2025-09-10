import os
from dotenv import load_dotenv
import pandas as pd
import psycopg
import pandas as pd

# Load environment variables
load_dotenv()

class MyDB:
    def __init__(self):
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.host = os.getenv("HOST")
        self.dbname = os.getenv("DATABASE")
        self.connection = None
    
    def connect(self):
        try:
            self.connection = psycopg.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
        
        except psycopg.OperationalError as oe:
            print("❌ Operational error: Could not connect to the database.")
            print("Details:", oe)

        except psycopg.DatabaseError as de:
            print("❌ Database error occurred.")
            print("Details:", de)

        except Exception as e:
            print("❌ Unexpected error:", e)

    def close(self):
        if self.connection:
            self.connection.close()
    
    def query_to_df(self, sql, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params or {})
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(rows, columns = columns)
        except psycopg.DatabaseError as e:
            error, = e.args
            print(f"❌ SQL execution failed: {error.message}")
            return pd.DataFrame()
