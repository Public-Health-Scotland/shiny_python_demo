import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

csv_path = "data/WHR2024.csv"
db_path = "data/encrypted_data.duckdb"
encryption_key = os.getenv("DUCKDB_KEY")

# Start in-memory DuckDB
con = duckdb.connect()

# Attach encrypted database
con.execute(f"""
    INSTALL httpfs;
    LOAD httpfs;
    ATTACH '{db_path}' AS enc (
        ENCRYPTION_KEY '{encryption_key}',
        ENCRYPTION_CIPHER 'GCM'
    );
    USE enc;
""")

# Import CSV
con.execute(f"""
    CREATE TABLE whr2024 AS
    SELECT *
    FROM read_csv_auto('{csv_path}');
""")

print("Successfully created encrypted DuckDB file and imported data.")

con.close()

# Open DuckDB with no file
con = duckdb.connect()

# attach encrypted duckdb file but read only
con.execute(f"""
    INSTALL httpfs;
    LOAD httpfs;
    ATTACH '{db_path}' AS enc (
        READ_ONLY,
        ENCRYPTION_KEY '{encryption_key}',
        ENCRYPTION_CIPHER 'GCM'
    );
    USE enc;
""")

df = con.execute('SELECT Year, "Country name", "Ladder score", "Explained by: Log GDP per capita" FROM whr2024').fetchdf()

con.close()

print(df)
print(df.dtypes)
