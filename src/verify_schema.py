import duckdb

con = duckdb.connect("data/analytics.db")
tables = con.execute("SHOW TABLES").fetchall()

for t in tables:
    name = t[0]
    print(f"\n--- {name} ---")
    cols = con.execute(f"DESCRIBE {name}").fetchall()
    for col in cols:
        print(f"  {col[0]:25} {col[1]}")

con.close()