import duckdb
import os

DB_PATH = "data/analytics.db"

def load_tpch(scale_factor=0.1):
    os.makedirs("data", exist_ok=True)
    con = duckdb.connect(DB_PATH)
    
    print("Loading TPC-H dataset...")
    con.execute(f"INSTALL tpch")
    con.execute(f"LOAD tpch")
    con.execute(f"CALL dbgen(sf={scale_factor})")
    
    tables = con.execute("SHOW TABLES").fetchall()
    print(f"\nTables created:")
    for t in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
        print(f"  {t[0]}: {count:,} rows")
    
    con.close()
    print("\nDone! Database saved to", DB_PATH)

if __name__ == "__main__":
    load_tpch()