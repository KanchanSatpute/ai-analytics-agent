import streamlit as st
import plotly.io as pio
import sys
sys.path.insert(0, "src")
from src.agent import run_query

st.set_page_config(page_title="AI Analytics Agent", page_icon="📊", layout="wide")
st.title("📊 AI Analytics Agent")
st.caption("Ask business questions in plain English — powered by GPT-4.1 + DuckDB TPC-H")

EXAMPLES = [
    "What are the top 5 nations by total revenue?",
    "Which market segment places the most orders?",
    "What is the monthly order trend for 1997?",
    "Which supplier has the highest total supply value?",
    "What percentage of line items were returned?",
]

with st.sidebar:
    st.header("Example questions")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state["question"] = ex

if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("chart") and not st.session_state.is_thinking:
            try:
                fig = pio.from_json(msg["chart"])
                st.plotly_chart(fig, use_container_width=True, key=f"history_chart_{i}")
            except Exception as e:
                print(f"Chart history render error: {e}")

question = st.chat_input("Ask a question about the data...")
if "question" in st.session_state:
    question = st.session_state.pop("question")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = run_query(question)
        st.write(result["answer"])
        if result["chart"]:
            try:
                fig = pio.from_json(result["chart"])
                st.plotly_chart(fig, use_container_width=True, key=f"new_chart_{len(st.session_state.messages)}")
            except Exception as e:
                print(f"Chart render error: {e}")
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "chart": result["chart"]
    })
    st.rerun()