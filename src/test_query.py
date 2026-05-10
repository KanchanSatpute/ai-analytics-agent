import duckdb

con = duckdb.connect("data/analytics.db")

result = con.execute("""
    SELECT n.n_name AS nation,
           ROUND(SUM(l.l_extendedprice * (1 - l.l_discount)), 2) AS revenue
    FROM lineitem l
    JOIN orders o ON l.l_orderkey = o.o_orderkey
    JOIN customer c ON o.o_custkey = c.c_custkey
    JOIN nation n ON c.c_nationkey = n.n_nationkey
    GROUP BY n.n_name
    ORDER BY revenue DESC
    LIMIT 5
""").df()

print(result)
con.close()