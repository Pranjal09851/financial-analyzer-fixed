## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader

# simple PDF loader helper
def load_pdf(path: str):
    """Return pages of text from a PDF file using LangChain's loader."""
    loader = PyPDFLoader(path)
    return loader.load()

# minimal search tool placeholder; real implementation can be added later
search_tool = None

class FinancialDocumentTool:
    @staticmethod
    async def read_data_tool(path: str = 'data/sample.pdf'):
        """Read all text from a PDF at `path` and return as a single string."""
        docs = load_pdf(path)
        full_report = []
        for page in docs:
            text = page.page_content
            # normalize whitespace
            text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            full_report.append(text)
        return "\n".join(full_report)