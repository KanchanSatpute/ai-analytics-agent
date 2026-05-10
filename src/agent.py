from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import json
from src.tools import get_schema, run_sql, generate_chart
from src.prompts import SYSTEM_PROMPT

load_dotenv()

TOOLS = [get_schema, run_sql, generate_chart]

def build_agent():
    llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(llm, TOOLS, prompt)
    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        return_intermediate_steps=True  # add this line
    )

def run_query(question: str) -> dict:
    executor = build_agent()
    result = executor.invoke({"input": question})
    output = result.get("output", "")
    
    chart_json = None
    for step in result.get("intermediate_steps", []):
        action, obs = step
        if getattr(action, "tool", "") == "generate_chart":
            chart_json = obs
            break

    return {"answer": output, "chart": chart_json}

if __name__ == "__main__":
    q = "What are the top 5 nations by total revenue?"
    result = run_query(q)
    print("\n=== ANSWER ===")
    print(result["answer"])
    print("\n=== CHART ===", "Generated" if result["chart"] else "None")