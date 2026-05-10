# 📊 AI Analytics Agent

A production-grade natural language analytics agent that converts plain English business questions into SQL queries, executes them against a local DuckDB database, and returns answers with auto-generated charts, no SQL knowledge required.

Built to demonstrate **agentic AI**, **LLM tool use**, **prompt engineering**, and **eval methodology** skills.

---

## 🎥 Demo

> Ask a question → Agent reasons → Writes SQL → Runs query → Returns answer + chart

![Demo](assets/demo.gif)


---

## 🏗️ Architecture

```
User Question (natural language)
        │
        ▼
┌─────────────────────┐
│   LangChain Agent   │  ← GPT-4.1-nano via OpenAI API
│  (ReAct reasoning)  │
└─────────────────────┘
        │
        ├──► get_schema()       ← Inspects available tables & columns
        │
        ├──► run_sql(query)     ← Executes DuckDB SQL, returns markdown table
        │
        └──► generate_chart()   ← Builds Plotly bar/line/pie chart
                │
                ▼
    ┌─────────────────────┐
    │    Streamlit UI     │  ← Chat interface with answer + interactive chart
    └─────────────────────┘
```

**Key design decisions:**
- The agent always inspects the schema before writing SQL — prevents hallucinated column names
- Chart generation is decoupled from SQL execution — the same query result can be both tabulated and visualized
- All data stays local (DuckDB) — no external database, no cloud dependency

---

## 📦 Dataset — TPC-H Benchmark

This project uses the **TPC-H** benchmark dataset, an industry-standard e-commerce simulation used by data engineers and database vendors worldwide. It is generated locally via DuckDB's built-in `dbgen` utility, no download required.

### Scale Factor
| Setting | Rows (approx) | Size |
|---------|--------------|------|
| `sf=0.1` (this project) | ~1M rows | ~100MB |
| `sf=1.0` | ~10M rows | ~1GB |

### Schema — 8 Tables

#### `orders` — Customer purchase orders
| Column | Type | Description |
|--------|------|-------------|
| o_orderkey | BIGINT | Primary key |
| o_custkey | BIGINT | Foreign key → customer |
| o_orderstatus | VARCHAR | O=open, F=fulfilled, P=pending |
| o_totalprice | DECIMAL | Total order value |
| o_orderdate | DATE | Date order was placed |
| o_orderpriority | VARCHAR | 1-URGENT to 5-LOW |
| o_clerk | VARCHAR | Clerk who processed order |
| o_shippriority | INTEGER | Shipping priority flag |

#### `lineitem` — Individual line items within orders
| Column | Type | Description |
|--------|------|-------------|
| l_orderkey | BIGINT | Foreign key → orders |
| l_partkey | BIGINT | Foreign key → part |
| l_suppkey | BIGINT | Foreign key → supplier |
| l_quantity | DECIMAL | Quantity ordered |
| l_extendedprice | DECIMAL | Line item price |
| l_discount | DECIMAL | Discount applied (0.0–0.1) |
| l_tax | DECIMAL | Tax rate |
| l_returnflag | VARCHAR | R=returned, A=accepted, N=not yet billed |
| l_linestatus | VARCHAR | O=open, F=final |
| l_shipdate | DATE | Actual ship date |

#### `customer` — Customer master data
| Column | Type | Description |
|--------|------|-------------|
| c_custkey | BIGINT | Primary key |
| c_name | VARCHAR | Customer name |
| c_nationkey | INTEGER | Foreign key → nation |
| c_acctbal | DECIMAL | Account balance |
| c_mktsegment | VARCHAR | BUILDING, AUTOMOBILE, MACHINERY, HOUSEHOLD, FURNITURE |

#### `supplier` — Supplier master data
| Column | Type | Description |
|--------|------|-------------|
| s_suppkey | BIGINT | Primary key |
| s_name | VARCHAR | Supplier name |
| s_nationkey | INTEGER | Foreign key → nation |
| s_acctbal | DECIMAL | Account balance |

#### `part` — Product catalog
| Column | Type | Description |
|--------|------|-------------|
| p_partkey | BIGINT | Primary key |
| p_name | VARCHAR | Part name |
| p_mfgr | VARCHAR | Manufacturer |
| p_brand | VARCHAR | Brand |
| p_type | VARCHAR | Part type |
| p_retailprice | DECIMAL | Retail price |

#### `partsupp` — Part-supplier mapping (inventory)
| Column | Type | Description |
|--------|------|-------------|
| ps_partkey | BIGINT | Foreign key → part |
| ps_suppkey | BIGINT | Foreign key → supplier |
| ps_availqty | BIGINT | Available quantity |
| ps_supplycost | DECIMAL | Cost per unit |

#### `nation` — Country reference
| Column | Type | Description |
|--------|------|-------------|
| n_nationkey | INTEGER | Primary key |
| n_name | VARCHAR | Country name (25 nations) |
| n_regionkey | INTEGER | Foreign key → region |

#### `region` — Regional groupings
| Column | Type | Description |
|--------|------|-------------|
| r_regionkey | INTEGER | Primary key |
| r_name | VARCHAR | AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST |

### Key Business Metrics
- **Revenue** = `l_extendedprice * (1 - l_discount)`
- **Supply value** = `ps_supplycost * ps_availqty`
- **Return rate** = % of line items where `l_returnflag = 'R'`

---

## 🤖 Agent Design

### Tools
| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `get_schema` | Returns all table/column definitions | None | Schema string |
| `run_sql` | Executes a DuckDB SQL query | SQL string | Markdown table |
| `generate_chart` | Creates a Plotly visualization | SQL + chart config | Plotly JSON |

### Reasoning Pattern
The agent follows a strict ReAct (Reasoning + Acting) loop:
1. **Inspect** — always calls `get_schema` first to ground SQL in real column names
2. **Query** — writes and executes SQL via `run_sql`
3. **Visualize** — calls `generate_chart` for comparison/trend/ranking questions
4. **Synthesize** — returns a 2-3 sentence business narrative

### Prompt Engineering
The system prompt encodes:
- Workflow order (schema → SQL → chart → summary)
- TPC-H field semantics (e.g. `l_returnflag` values)
- Formatting rules (no LaTeX, no markdown symbols in answers)
- Revenue formula to ensure correct calculations

---

## 📈 Eval Results

Tested against 3 business questions spanning joins, aggregations, and counting queries.

| Test | Question | Status |
|------|----------|--------|
| 1 | Top 3 nations by revenue | ✅ PASS |
| 2 | Total orders placed | ✅ PASS |
| 3 | Average order value | ✅ PASS |

**Score: 3/3**

Eval methodology: each question is checked against a lambda function that validates key terms or numeric presence in the agent's answer. See `tests/eval.py` for full test cases.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | GPT-4.1-nano (OpenAI) |
| Agent framework | LangChain 0.3 (tool-calling agent) |
| Database | DuckDB 1.2 |
| Data manipulation | pandas, numpy |
| Visualization | Plotly |
| UI | Streamlit |
| Python | 3.13 |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.13
- OpenAI API key (get one at platform.openai.com)

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-analytics-agent.git
cd ai-analytics-agent

# Create and activate virtual environment
python3.13 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Load the TPC-H dataset into DuckDB
python src/load_data.py

# Launch the app
streamlit run app.py
```

Open your browser at `http://localhost:8501`

### Run the eval suite
```bash
python tests/eval.py
```

---

## 📁 Project Structure

```
ai-analytics-agent/
├── src/
│   ├── agent.py          ← LangChain agent with tool-calling
│   ├── tools.py          ← get_schema, run_sql, generate_chart
│   ├── prompts.py        ← System prompt and field reference
│   ├── load_data.py      ← TPC-H dataset loader
│   └── verify_schema.py  ← Schema inspection utility
├── notebooks/
│   └── 01_agent_demo.ipynb  ← Interactive demo notebook
├── tests/
│   └── eval.py           ← Eval suite with scored test cases
├── data/
│   └── analytics.db      ← DuckDB database (generated locally)
├── app.py                ← Streamlit chat UI
├── requirements.txt
└── .env                  ← API keys (never committed)
```

---

## 💡 Example Questions

Try these in the chat interface:

**Revenue & Sales**
- "What are the top 5 nations by total revenue?"
- "What is the average order value?"
- "Which region generates the most revenue?"

**Operations**
- "What percentage of line items were returned?"
- "Which market segment places the most orders?"
- "What is the monthly order trend for 1997?"

**Supply Chain**
- "Which supplier has the highest total supply value?"
- "What are the top 10 most expensive parts?"
- "Which nation has the most suppliers?"

---

## 🔭 Future Improvements

- [ ] Add memory so the agent can handle follow-up questions in context
- [ ] Expand eval suite to 20+ questions covering all 8 tables
- [ ] Add hallucination detection — flag answers where SQL result contradicts the narrative
- [ ] Support uploading custom CSV files for ad-hoc analysis
- [ ] Add query history and export to CSV

---
