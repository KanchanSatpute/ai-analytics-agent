from tools import get_schema, run_sql, generate_chart

# Test 1 — schema
print("=== SCHEMA ===")
print(get_schema.invoke({}))

# Test 2 — SQL
print("\n=== SQL RESULT ===")
print(run_sql.invoke({
    "query": "SELECT l_returnflag, COUNT(*) as cnt FROM lineitem GROUP BY 1"
}))

# Test 3 — chart
print("\n=== CHART (json length) ===")
result = generate_chart.invoke({
    "query": "SELECT n_name, COUNT(*) as cnt FROM nation GROUP BY 1",
    "chart_type": "bar",
    "x_col": "n_name",
    "y_col": "cnt",
    "title": "Nations"
})
print(f"Chart JSON length: {len(result)} chars")