import duckdb
import pandas as pd
import plotly.express as px
from langchain_core.tools import tool
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "analytics.db")

def get_connection():
    return duckdb.connect(DB_PATH, read_only=True)

@tool
def get_schema() -> str:
    """Returns the database schema: all table names and their columns.
    Always call this first before writing any SQL query."""
    con = get_connection()
    tables = con.execute("SHOW TABLES").fetchall()
    schema = []
    for t in tables:
        name = t[0]
        cols = con.execute(f"DESCRIBE {name}").fetchall()
        col_str = ", ".join([f"{c[0]} ({c[1]})" for c in cols])
        schema.append(f"{name}: {col_str}")
    con.close()
    return "\n".join(schema)

@tool
def run_sql(query: str) -> str:
    """Executes a DuckDB SQL query and returns results as a markdown table.
    Use this to answer analytical questions. Always inspect the schema first."""
    try:
        con = get_connection()
        df = con.execute(query).df()
        con.close()
        if df.empty:
            return "Query returned no results."
        return df.to_markdown(index=False)
    except Exception as e:
        return f"SQL Error: {str(e)}"

@tool
def generate_chart(query: str, chart_type: str = "bar",
                   x_col: str = "", y_col: str = "",
                   title: str = "") -> str:
    """Runs a SQL query and generates a Plotly chart from the results.
    chart_type options: bar, line, pie.
    Returns a JSON string of the Plotly figure."""
    try:
        con = get_connection()
        df = con.execute(query).df()
        con.close()
        if df.empty:
            return "No data to chart."
        x = x_col or df.columns[0]
        y = y_col or df.columns[1]
        if chart_type == "line":
            fig = px.line(df, x=x, y=y, title=title)
        elif chart_type == "pie":
            fig = px.pie(df, names=x, values=y, title=title)
        else:
            df[x] = df[x].astype(str)
            fig = px.bar(df, x=x, y=y, title=title)
            fig.update_traces(width=0.4)
            fig.update_layout(bargap=0.1)
        return fig.to_json()
    except Exception as e:
        return f"Chart Error: {str(e)}"