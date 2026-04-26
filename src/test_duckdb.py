import duckdb

con = duckdb.connect("data/sample.db")

con.execute("""
  CREATE TABLE IF NOT EXISTS orders AS
  SELECT * FROM range(100) AS t(order_id),
  (SELECT random() * 1000 AS revenue) sub
""")

result = con.execute("SELECT COUNT(*), AVG(revenue) FROM orders").fetchall()
print(result)  # [(100, ~500.0)]