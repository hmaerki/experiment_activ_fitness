# Activ Fitness

A web-based fitness training plan application built with [PyScript](https://pyscript.net/), which enables Python to run directly in the browser via WebAssembly (WASM).

Run it: https://hmaerki.github.io/activ_fitness

## Features

- **Workouts list** – shows all recorded workout sessions with progress (done/total exercises)
- **Workout view** – lists all exercises for a session; completed exercises are greyed out
- **Exercise detail** – shows machine settings, lets you update the weight and mark the exercise as done

All data is persisted in the browser's `localStorage` – no backend required.

## Running locally

Open `index.html` in a browser served over HTTP (required for PyScript's module loading), for example:

```bash
python -m http.server 8000
```

Then navigate to `http://localhost:8000`.

## Project structure

```
experiment_activ_fitness/
├── assets/
│   └── exercises.py   # training-plan template
├── index.html           # single-page app shell + CSS
├── main.py              # PyScript application logic
├── pyscript.toml        # PyScript configuration
└── README.md
```
