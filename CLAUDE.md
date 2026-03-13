# Claude Instructions

## Project Overview

`experiment_activ_fitness` is a web-based fitness training plan application built with [PyScript](https://pyscript.net/), which enables Python to run directly in the browser via WebAssembly (WASM). There is no backend server – all logic runs client-side.

## Repository Layout

```
experiment_activ_fitness/
├── index.html          # Main HTML entry point, loads PyScript
├── main.py             # Application logic written in Python (runs via PyScript/WASM)
├── requirements.txt    # Python dependencies for Pyodide/PyScript
├── tests/              # pytest unit tests
├── .github/
│   └── copilot-instructions.md
├── CLAUDE.md           # This file
└── README.md
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | HTML5, CSS3 |
| App logic | Python 3.11+ via PyScript (Pyodide WASM) |
| Testing | pytest, playwright (browser tests) |
| Formatting | Black (line length 88) |

## Domain Model

- **TrainingPlan**: Top-level container holding multiple weeks
- **Week**: A 7-day block within the plan
- **Day**: A single calendar day, containing zero or more exercises
- **Exercise**: One activity entry – type (run/cycle/swim/gym), duration (minutes), intensity (1–10), optional notes

## Coding Guidelines

### Python

- Use **type hints** on all public functions and methods
- Format with **Black** (`black --line-length 88`)
- Lint with **flake8** or **ruff**
- `snake_case` for names, `PascalCase` for classes, `UPPER_CASE` for module-level constants
- PyScript DOM access via `from pyscript import document` or the `js` bridge
- Use `async def` + `await` for any operation that must not block the browser event loop

### HTML / CSS

- Semantic HTML5 elements (`<main>`, `<section>`, `<article>`, etc.)
- CSS custom properties for colours and spacing
- Minimal inline `<script>` – prefer Python for logic

## Running Locally

Open `index.html` directly in a browser (a local HTTP server is recommended because
browsers restrict `file://` origins for WASM):

```bash
python -m http.server 8080
# then open http://localhost:8080
```

## Running Tests

```bash
pytest tests/
```

## Constraints & Gotchas

1. **PyPI packages**: only packages bundled with [Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) or pure-Python wheels are available
2. **No Node.js / npm** – this is a pure-Python + HTML project
3. **CORS**: when fetching external resources from PyScript, ensure CORS headers are present
4. **File size**: keep total page weight low; Pyodide itself is already several MB
