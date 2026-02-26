## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from tools import FinancialDocumentTool

# simple configuration for the LLM used by all agents
LLM_MODEL = "gpt-4o-mini"

# single financial analyst agent with reasonable settings
financial_analyst = Agent(
    role="Financial Analyst",
    goal="Analyze the PDF financial document at {pdf_path} and extract key metrics",
    verbose=True,
    backstory="You are an experienced financial analyst who provides accurate, concise, and factual information.",
    llm=LLM_MODEL,
    max_iter=2,
    allow_delegation=False,
)

# the crew may be extended with other agents as needed, but for now we only use the analyst
agents = [financial_analyst]
