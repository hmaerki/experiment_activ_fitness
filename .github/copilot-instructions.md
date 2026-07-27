# Copilot Instructions

## Project Overview

`experiment_activ_fitness` is a web-based fitness training plan application built with [PyScript](https://pyscript.net/), which enables Python to run directly in the browser via WebAssembly (WASM).

## Tech Stack

- **Frontend**: HTML, CSS (minimal JavaScript). Use this as a base: https://github.com/pyscript/docs/tree/main/docs/example-apps/task-board-web
- **Python runtime**: PyScript (WASM-based in-browser Python)
- **Persistent data**:  https://docs.pyscript.net/2026.3.1/api/storage/
- **No backend server** – everything runs client-side in the browser

## Project Structure

Use this as a base: https://github.com/pyscript/examples/tree/main/tic-tac-toe

```
experiment_activ_fitness/
├── assets/
│   └── exercises.json
├── index.html
├── main.py
├── pyscript.toml
└── README.md
```

## Coding Conventions

### Python (PyScript)

- Target **Python 3.13+** syntax
- Use type hints for function signatures
- Keep PyScript-specific DOM manipulation in clearly named helper functions
- Prefer `pyscript` and `pyodide` APIs for browser interaction over raw JavaScript interop when possible
- If possible use `pyscript-micropython`
- Format code with [Black](https://black.readthedocs.io/) (line length 88)
- Use `snake_case` for variables and functions, `PascalCase` for classes

### HTML / JavaScript

- Use semantic HTML5 elements
- Keep inline JavaScript minimal; prefer PyScript for application logic
- Use CSS custom properties (variables) for theming

## Key Domain Concepts

- **Training plan**: This is given in `assets/exercises.json`

## Web pages

- **Workouts**: A list of dates when a workout was executed.
    Top of page: Button "New workout".
    "New workout" creates a new workout for the current date and copies the exercise values from the most recent previous workout so the new session starts with the latest known settings.
- **Workout**: Lists exercises: `key` and `short` from from `assets/exercises.json`.
    Already executed exercises are grayed out.
    When clicking on a exercise, the excercise page opens.
- **Excercise**: 
    Displays the details of the exercise.
    Button `Done` marks the exercise as done. Add a new key `done` to exercises.json in the local storage.
    Button `Cancel` closes the page.
    The `weight` might be changed and stored in the local storage.

## Testing

- Python unit tests live in `tests/` and are run with `pytest`
- Browser integration tests (if any) use `playwright`

## Important Notes

- PyScript loads Python packages from PyPI via Pyodide; only packages available in [Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) or pure-Python wheels can be used
- Avoid browser-blocking operations; use `async/await` with PyScript's async support for long-running tasks
- When manipulating the DOM from Python, use `from pyscript import document` or the `js` module
