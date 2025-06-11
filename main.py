import typer
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from content_evaluator import ContentEvaluator
import sys
import os

app = FastAPI(title="Content Evaluation API")
evaluator = ContentEvaluator()

# Create templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)

# Set up templates
templates = Jinja2Templates(directory="templates")

class ContentSubmission(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/evaluate")
async def evaluate_content(submission: ContentSubmission):
    try:
        result = evaluator.evaluate_submission(submission.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CLI interface
cli = typer.Typer()

@cli.command()
def evaluate(text: str):
    """Evaluate content from the command line."""
    try:
        print("\nEvaluating content...\n")
        result = evaluator.evaluate_submission(text)
        
        # Print scores
        print("Scores:")
        print("-" * 50)
        for criterion, score in result["scores"].items():
            print(f"{criterion.replace('_', ' ').title()}: {score}/5")
        
        # Print feedback
        print("\nFeedback:")
        print("-" * 50)
        for criterion, feedback in result["feedback"].items():
            print(f"{criterion.replace('_', ' ').title()}: {feedback}")
        
        # Print summary
        print("\nSummary:")
        print("-" * 50)
        print(f"Total Score: {result['total_score']}/30")
        print(f"Verdict: {result['verdict']}")
        
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)

def start_server():
    """Start the FastAPI server."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "evaluate":
        cli()
    else:
        start_server() 