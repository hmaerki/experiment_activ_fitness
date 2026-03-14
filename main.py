from pyscript import document, when
from exercises import EXERCISES
import json
import js
from datetime import datetime

STORAGE_KEY = "activ_fitness_workouts"


class FitnessApp:
    def __init__(self, exercises_template: dict) -> None:
        self.exercises_template = exercises_template
        self.workouts: dict = {}
        self.current_workout_date: str | None = None
        self.current_exercise_key: str | None = None

        stored = js.localStorage.getItem(STORAGE_KEY)
        if stored:
            self.workouts = json.loads(stored)

        when("click", "#btn-new-workout")(self.new_workout)
        when("click", "#btn-back-to-workouts")(self.show_workouts)
        when("click", "#btn-done")(self.done_exercise)
        when("click", "#btn-cancel")(self.cancel_exercise)
        when("click", "#btn-delete-workout")(self.delete_workout)
        when("click", "#workouts-list")(self._on_workout_click)
        when("click", "#exercises-list")(self._on_exercise_click)

        self.show_workouts()

    def _save(self) -> None:
        js.localStorage.setItem(STORAGE_KEY, json.dumps(self.workouts))

    def _show_view(self, view_id: str) -> None:
        for vid in ("view-workouts", "view-workout", "view-exercise"):
            el = document.getElementById(vid)
            if vid == view_id:
                el.removeAttribute("hidden")
            else:
                el.setAttribute("hidden", "hidden")

    def show_workouts(self, event=None) -> None:
        self._show_view("view-workouts")
        container = document.getElementById("workouts-list")
        container.innerHTML = ""

        if not self.workouts:
            li = document.createElement("li")
            li.textContent = "No workouts yet. Click 'New workout' to start!"
            li.className = "empty-hint"
            container.appendChild(li)
            return

        for date_str in sorted(self.workouts.keys(), reverse=True):
            workout = self.workouts[date_str]
            done_count = sum(1 for ex in workout.values() if ex.get("done"))
            total = len(workout)

            li = document.createElement("li")
            li.className = "workout-item"
            li.setAttribute("data-date", date_str)

            span_date = document.createElement("span")
            span_date.className = "workout-date"
            span_date.textContent = date_str

            span_progress = document.createElement("span")
            span_progress.className = "workout-progress"
            span_progress.textContent = f"{done_count}/{total} done"

            li.appendChild(span_date)
            li.appendChild(span_progress)
            container.appendChild(li)

    def new_workout(self, event=None) -> None:
        date_str = datetime.now().strftime("%Y-%m-%d")
        self.workouts[date_str] = json.loads(json.dumps(self.exercises_template))
        self._save()
        self.show_workout(date_str)

    def _on_workout_click(self, event) -> None:
        target = event.target.closest(".workout-item")
        if target:
            date_str = str(target.getAttribute("data-date"))
            self.show_workout(date_str)

    def show_workout(self, date_str: str) -> None:
        self.current_workout_date = date_str
        self._show_view("view-workout")
        document.getElementById("workout-date").textContent = date_str

        container = document.getElementById("exercises-list")
        container.innerHTML = ""

        workout = self.workouts[date_str]
        for key, exercise in workout.items():
            li = document.createElement("li")
            li.className = "exercise-item" + (" done" if exercise.get("done") else "")
            li.setAttribute("data-key", key)

            span_key = document.createElement("span")
            span_key.className = "exercise-key"
            span_key.textContent = key

            span_name = document.createElement("span")
            span_name.className = "exercise-name"
            span_name.textContent = exercise["short"]

            li.appendChild(span_key)
            li.appendChild(span_name)
            container.appendChild(li)

    def _on_exercise_click(self, event) -> None:
        target = event.target.closest(".exercise-item")
        if target:
            key = str(target.getAttribute("data-key"))
            self.show_exercise(key)

    def show_exercise(self, exercise_key: str) -> None:
        self.current_exercise_key = exercise_key
        self._show_view("view-exercise")

        exercise = self.workouts[self.current_workout_date][exercise_key]
        document.getElementById("exercise-key").textContent = exercise_key
        document.getElementById("exercise-short").textContent = exercise.get(
            "short", ""
        )
        document.getElementById("exercise-comment").textContent = exercise.get(
            "comment", ""
        )
        document.getElementById("exercise-weight").value = str(
            exercise.get("weight", "")
        )
        document.getElementById("exercise-set1").value = str(
            exercise.get("set1", 15)
        )
        document.getElementById("exercise-set2").value = str(
            exercise.get("set2", 15)
        )

        card = document.getElementById("exercise-detail-card")
        if exercise.get("done"):
            card.classList.add("done")
        else:
            card.classList.remove("done")

        btn_done = document.getElementById("btn-done")
        SVG_LEFT = '<svg width="22" height="22"><use href="#arrow-left"/></svg>'
        SVG_RIGHT = '<svg width="22" height="22"><use href="#arrow-right"/></svg>'
        if exercise.get("done"):
            btn_done.innerHTML = f'{SVG_LEFT} Undo Done'
        else:
            btn_done.innerHTML = f'Done {SVG_RIGHT}'

    def done_exercise(self, event=None) -> None:
        exercise = self.workouts[self.current_workout_date][self.current_exercise_key]

        weight_val = str(document.getElementById("exercise-weight").value)
        if weight_val:
            try:
                exercise["weight"] = float(weight_val)
            except (ValueError, TypeError):
                pass

        reps_val = str(document.getElementById("exercise-set1").value)
        if reps_val:
            try:
                exercise["set1"] = int(reps_val)
            except (ValueError, TypeError):
                pass
        reps_val = str(document.getElementById("exercise-set2").value)
        if reps_val:
            try:
                exercise["set2"] = int(reps_val)
            except (ValueError, TypeError):
                pass

        exercise["done"] = not exercise.get("done", False)
        self._save()
        self.show_workout(self.current_workout_date)

    def cancel_exercise(self, event=None) -> None:
        self.show_workout(self.current_workout_date)

    def delete_workout(self, event=None) -> None:
        if self.current_workout_date in self.workouts:
            del self.workouts[self.current_workout_date]
            self._save()
        self.show_workouts()


APP = FitnessApp(EXERCISES)
