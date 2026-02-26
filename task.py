## Importing libraries and files
from crewai import Task

from agents import financial_analyst
from tools import FinancialDocumentTool

## primary analysis task: read pdf and output structured JSON
analyze_financial_document = Task(
    description="""
Analyze the financial PDF located at {pdf_path}.
Return output strictly as JSON with keys: revenue, ebitda, debt_equity, risks (list), recommend (str).
""",
    expected_output="""{"revenue": float, "ebitda": float, "debt_equity": float, "risks": [], "recommend": ""}""",
    agent=financial_analyst,
    async_execution=False,
)

# bundle tasks for easy import
TASKS = [analyze_financial_document]