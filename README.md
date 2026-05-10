# AI Analytics Agent

A natural language analytics agent that converts plain English questions
into SQL queries, executes them against a local DuckDB database, and returns
answers with auto-generated charts.

Built to demonstrate agentic AI, LLM tool use, and production-grade
eval methodology — skills directly relevant to data science roles at
AI-first companies.

## Demo


## Architecture
User question → LangChain agent → get_schema tool → run_sql tool
→ generate_chart tool → natural language answer + Plotly chart

## Tech stack
- LangChain tool-calling agent (ReAct pattern)
- GPT-4.1-nano via OpenAI API
- DuckDB (TPC-H benchmark dataset, ~1M rows)
- Streamlit for the chat UI
- Plotly for chart generation

## Eval results
Tested against 10 business questions spanning joins, aggregations,
time-series, and ranking queries. Score: X/10.

## Run locally
git clone https://github.com/YOUR_USERNAME/ai-analytics-agent <br>
cd ai-analytics-agent <br>
python -m venv .venv && source .venv/bin/activate <br>
pip install -r requirements.txt <br>
echo "OPENAI_API_KEY=your-key" > .env <br>
python src/load_data.py <br>
streamlit run app.py <br>
