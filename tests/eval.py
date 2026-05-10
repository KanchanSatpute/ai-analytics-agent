import sys, os, duckdb
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent import run_query

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "analytics.db")
con = duckdb.connect(DB_PATH, read_only=True)

EVAL_CASES = [
    {
        "question": "What are the top 3 nations by revenue?",
        "expected_sql": """SELECT n.n_name, ROUND(SUM(l.l_extendedprice*(1-l.l_discount)),2) as revenue
                           FROM lineitem l JOIN orders o ON l.l_orderkey=o.o_orderkey
                           JOIN customer c ON o.o_custkey=c.c_custkey
                           JOIN nation n ON c.c_nationkey=n.n_nationkey
                           GROUP BY 1 ORDER BY 2 DESC LIMIT 3""",
        "check": lambda ans: any(word in ans.lower() for word in ["nation", "revenue", "top"])
    },
    {
        "question": "How many orders were placed in total?",
        "expected_sql": "SELECT COUNT(*) FROM orders",
        "check": lambda ans: any(c.isdigit() for c in ans)
    },
    {
        "question": "What is the average order value?",
        "expected_sql": "SELECT ROUND(AVG(o_totalprice), 2) FROM orders",
        "check": lambda ans: any(c.isdigit() for c in ans)
    },
]

def run_eval():
    results = []
    for i, case in enumerate(EVAL_CASES):
        print(f"\nTest {i+1}: {case['question']}")
        result = run_query(case["question"])
        passed = case["check"](result["answer"])
        status = "PASS" if passed else "FAIL"
        print(f"  Status: {status}")
        print(f"  Answer: {result['answer'][:100]}...")
        results.append(passed)
    score = sum(results)
    print(f"\n=== Score: {score}/{len(results)} ===")
    return score

if __name__ == "__main__":
    run_eval()