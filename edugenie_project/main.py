"""EduGenie: Google Gemini powered learning assistant."""
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie", description="An AI-powered educational learning assistant", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000, description="Question, topic, or educational passage")
    level: str = Field(default="Beginner", max_length=40)

class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=12000)
    level: str = Field(default="Beginner", max_length=40)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.get("/health")
def health():
    return {"status": "ok", "app": "EduGenie"}

@app.post("/qa")
def qa(payload: TextRequest):
    return _run(lambda: {"result": answer_question(payload.text, payload.level)})

@app.post("/explain")
def explain(payload: TextRequest):
    return _run(lambda: {"result": explain_concept(payload.text, payload.level)})

@app.post("/quiz")
def quiz(payload: QuizRequest):
    return _run(lambda: {"result": generate_quiz(payload.text, payload.level)})

@app.post("/summarize")
def summarize(payload: TextRequest):
    return _run(lambda: {"result": summarize_text(payload.text, payload.level)})

@app.post("/learn/recommendations")
def recommendations(payload: TextRequest):
    return _run(lambda: {"result": get_learning_recommendations(payload.text, payload.level)})

def _run(operation):
    try:
        return operation()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=f"The AI returned an invalid response: {exc}") from exc
    except Exception as exc:
        # Do not leak provider credentials or internal tracebacks to clients.
        raise HTTPException(status_code=502, detail=f"AI request failed. Check your API key, model name, and network connection. Details: {exc}") from exc
