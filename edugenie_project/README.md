# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a responsive educational assistant based on the supplied project document. It uses **FastAPI + Jinja2 + HTML/CSS/JavaScript** and exposes five API features:

- **Explain** a concept in simple language (optionally using the local LaMini-Flan-T5 model).
- **Q&A** for academic and general learning questions.
- **Quiz** generation: exactly three MCQs, each with four options, a correct answer, and an explanation. The frontend checks answers and reveals the correct answer when an option is selected.
- **Summarize** an educational passage.
- **Learning path** with staged topics, timelines, practice ideas, and resource suggestions.

The Gemini model name is configurable. This project defaults to `gemini-2.5-flash`; the source document mentions Gemini 1.5 Pro, but model availability can change. Set `GEMINI_MODEL` to a model currently available to your API key. The API key stays in `.env` and is not sent to the browser.

## Requirements

- Python 3.10 or newer
- Internet connection for Gemini calls and the first-time Python package installation
- Google AI Studio API key for AI-generated Q&A, quizzes, summaries, and learning paths
- VS Code (recommended)

## Run in VS Code (Windows)

1. Extract the ZIP file and open the `edugenie_project` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again. Alternatively use Command Prompt and run `.venv\\Scripts\\activate.bat`.
4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to a new file named `.env`. Add your key after `GEMINI_API_KEY=`. Obtain a key at https://aistudio.google.com/apikey. Do not share or commit `.env`.
6. Start the app:

   ```powershell
   uvicorn main:app --reload
   ```
7. Open **http://127.0.0.1:8000** in your browser. API docs are at **http://127.0.0.1:8000/docs** and health check at **http://127.0.0.1:8000/health**.
8. Stop the server with `Ctrl+C` in the terminal.

## Run on macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GEMINI_API_KEY
uvicorn main:app --reload
```

Then visit http://127.0.0.1:8000.

## Optional local explanation model

The document specifies `LaMini-Flan-T5-783M` for concept explanations. It is optional because downloading the model and installing PyTorch can use several GB of disk space and memory. To enable it:

1. Install the optional dependencies (choose a PyTorch build suitable for your system):

   ```bash
   pip install "transformers>=4.44,<5" torch
   ```
2. Set `ENABLE_LOCAL_EXPLAINER=true` in `.env`.
3. Restart Uvicorn. On the first explanation request, Hugging Face downloads the model. If local model loading fails, the app attempts Gemini instead.

When `GEMINI_API_KEY` is absent, the explain endpoint has a short demo fallback. The other Gemini-backed endpoints return a helpful configuration error. This fallback is not a substitute for AI inference.

## API reference

All POST endpoints accept JSON with `text` and optional `level` (`Beginner`, `Intermediate`, or `Advanced`).

| Method | Endpoint | Response |
|---|---|---|
| GET | `/` | Web app |
| GET | `/health` | Service status |
| POST | `/qa` | `{"result": "..."}` |
| POST | `/explain` | `{"result": "..."}` |
| POST | `/quiz` | `{"result": [{"question": "...", "options": ["..."], "answer": "...", "explanation": "..."}]}` |
| POST | `/summarize` | `{"result": "..."}` |
| POST | `/learn/recommendations` | `{"result": "..."}` |

Example request:

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"text":"Which is the largest ocean?","level":"Beginner"}'
```

PowerShell example:

```powershell
$body = @{ text = 'Which is the largest ocean?'; level = 'Beginner' } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/qa -Method Post -ContentType 'application/json' -Body $body
```

## Testing

With the virtual environment active:

```bash
pytest -q
```

Tests check the homepage, health endpoint, input validation, and the no-key explanation fallback. Tests do not call Gemini or verify the quality of live model output. To test real AI features, configure a valid key and use each feature in the browser or `/docs`.

## Project structure

```text
edugenie_project/
├── main.py                  # FastAPI app and REST endpoints
├── ai_client.py             # Shared Gemini client
├── explanation_module.py    # Simple concept explanations / optional local model
├── qna.py                   # Question answering
├── quiz_module.py            # Quiz generation and JSON validation
├── summary_module.py        # Summarization
├── learning_path.py         # Learning recommendations
├── templates/
│   └── index.html            # Responsive UI and browser-side quiz interaction
├── static/
│   └── style.css             # Responsive styling
├── tests/
│   └── test_api.py           # Automated smoke tests
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Troubleshooting

- **`GEMINI_API_KEY is not set`**: ensure `.env` is in the project root beside `main.py` and contains the key, then restart Uvicorn.
- **Invalid API key / permission / quota errors**: check the key and API access in Google AI Studio, your quota, and the selected `GEMINI_MODEL`.
- **`uvicorn` not found**: activate `.venv` and run `python -m pip install -r requirements.txt`; then use `python -m uvicorn main:app --reload`.
- **Port 8000 is busy**: run `uvicorn main:app --reload --port 8001` and open http://127.0.0.1:8001.
- **Quiz response rejected**: generation is validated to enforce three questions and four options each. Retry if the model returns malformed JSON.

## Safety and privacy notes

Do not submit passwords, API keys, or sensitive personal information in prompts. AI output can be inaccurate; verify important academic facts. This starter project does not store user history or implement user accounts.
