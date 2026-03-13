# Copilot Instructions

## Project Overview

`experiment_activ_fitness` is a web-based fitness training plan application built with [PyScript](https://pyscript.net/), which enables Python to run directly in the browser via WebAssembly (WASM).

## Tech Stack

- **Frontend**: HTML, CSS (minimal JavaScript)
- **Python runtime**: PyScript (WASM-based in-browser Python)
- **No backend server** – everything runs client-side in the browser

## Project Structure

```
experiment_activ_fitness/
├── index.html          # Main HTML entry point
├── main.py             # PyScript Python application code
├── requirements.txt    # Python package dependencies for PyScript
└── README.md
```

## Coding Conventions

### Python (PyScript)

- Target **Python 3.11+** syntax
- Use type hints for function signatures
- Keep PyScript-specific DOM manipulation in clearly named helper functions
- Prefer `pyscript` and `pyodide` APIs for browser interaction over raw JavaScript interop when possible
- Format code with [Black](https://black.readthedocs.io/) (line length 88)
- Use `snake_case` for variables and functions, `PascalCase` for classes

### HTML / JavaScript

- Use semantic HTML5 elements
- Keep inline JavaScript minimal; prefer PyScript for application logic
- Use CSS custom properties (variables) for theming

## Key Domain Concepts

- **Training plan**: A structured weekly schedule of fitness exercises
- **Exercise**: A single activity (e.g., running, cycling, strength training) with duration, intensity, and notes
- **Week / Day**: Organizational units within the training plan

## Testing

- Python unit tests live in `tests/` and are run with `pytest`
- Browser integration tests (if any) use `playwright`

## Important Notes

- PyScript loads Python packages from PyPI via Pyodide; only packages available in [Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) or pure-Python wheels can be used
- Avoid browser-blocking operations; use `async/await` with PyScript's async support for long-running tasks
- When manipulating the DOM from Python, use `from pyscript import document` or the `js` module
