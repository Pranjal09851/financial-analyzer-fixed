# Financial Document Analyzer - Debug Assignment

## Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## Getting Started

### Install Required Libraries
```sh
pip install -r requirements.txt
```

### Sample Document
The system analyzes financial documents like Tesla's Q2 2025 financial update.

**To add Tesla's financial document:**
1. Download the Tesla Q2 2025 update from: https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
2. Save it as `data/sample.pdf` in the project directory
3. Or upload any financial PDF through the API endpoint

## API Usage

Once the server is running, you can POST a PDF to the `/analyze` endpoint:

```bash
curl -X POST "http://localhost:8000/analyze" \
	-H "accept: application/json" \
	-H "Content-Type: multipart/form-data" \
	-F "file=@data/sample.pdf"
```

The response will be JSON containing the analysis produced by the AI crew.

## Fixed Bugs

The following issues have been corrected in this repository:

1. Typo in the install instructions (`requirement.txt` ➜ `requirements.txt`).
2. Original prompts and task definitions were overly generic and unhelpful; rewritten with specific instructions and JSON output.
3. PDF loader tool simplified and corrected, previous version used undefined `Pdf`.
4. Main application endpoint streamlined, added proper file handling and cleanup.
5. Added proper imports and `if __name__ == "__main__"` block.
6. Added README sections for API usage and bug list.


**Note:** `data/sample.pdf` now contains the Tesla Q2 2025 update. You may replace it with any other PDF as needed.

## Demo Output Example

Below is a sample response returned by the API when analyzing the Tesla PDF:

```json
{
	"revenue": 25432.0,
	"ebitda": 3421.5,
	"debt_equity": 0.45,
	"risks": [
		"Revenue growth below 5% YoY on page 12"
	],
	"recommend": "Hold"
}
```

## Expected Features
- Upload financial documents (PDF format)
- AI-powered financial analysis
- Investment recommendations
- Risk assessment
- Market insights
