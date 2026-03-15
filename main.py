from __future__ import annotations

from pyscript import document, when # type: ignore
import js # type: ignore
import application
import persistence


class FitnessApp:
    def __init__(self) -> None:
        print("FitnessApp()")
        self.persistence = persistence.Persistence()
        self.current_exercise: persistence.CurrentExercise | None = None
        self.current_workout_date: str = ""

        self._dom_update_who()

        when("click", "#btn-new-workout")(self.on_new_workout)
        when("click", "#who-name")(self.on_toggle_who)
        when("click", "#btn-back-to-workouts")(self.on_show_workouts)
        when("click", "#btn-done")(self.on_done_exercise)
        when("click", "#btn-cancel")(self.on_cancel_exercise)
        when("click", "#btn-delete-workout")(self.on_delete_workout)
        when("click", "#btn-show-json")(self.on_show_json)
        when("click", "#btn-back-from-json")(self.on_back_from_json)
        when("click", "#btn-save-json")(self.on_save_json)
        when("click", "#btn-delete-storage")(self.on_delete_storage)
        when("click", "#workouts-list")(self.on_workout_click)
        when("click", "#exercises-list")(self.on_exercise_click)

        self.on_show_workouts()

    def _dom_update_who(self) -> None:
        document.getElementById(
            "hans-im-glueck"
        ).src = f"./assets/{self.persistence.who.image}"
        document.getElementById("who-name").textContent = self.persistence.who.name

    def on_toggle_who(self, event=None) -> None:
        self.persistence.toggle_who()
        self._dom_update_who()

    def _dom_show_view(self, view_id: str) -> None:
        for vid in ("view-workouts", "view-workout", "view-exercise", "view-json"):
            el = document.getElementById(vid)
            if vid == view_id:
                el.removeAttribute("hidden")
            else:
                el.setAttribute("hidden", "hidden")

    def on_show_workouts(self, event=None) -> None:
        self._dom_show_view("view-workouts")
        container = document.getElementById("workouts-list")
        container.innerHTML = ""

        if not self.persistence.workouts.has_workouts:
            li = document.createElement("li")
            li.textContent = "No workouts yet. Click 'New workout' to start!"
            li.className = "empty-hint"
            container.appendChild(li)
            return

        for workout_date in self.persistence.workouts.workout_dates:
            li = document.createElement("li")
            li.className = "workout-item"
            li.setAttribute("workout-date", workout_date)

            span_date = document.createElement("span")
            span_date.className = "workout-date"
            span_date.textContent = workout_date

            span_progress = document.createElement("span")
            span_progress.className = "workout-progress"
            span_progress.textContent = self.persistence.workouts.get_progress(
                workout_date
            )

            li.appendChild(span_date)
            li.appendChild(span_progress)
            container.appendChild(li)

    def on_new_workout(self, event=None) -> None:
        d = js.Date.new()
        self.current_workout_date = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            d.getFullYear(),
            d.getMonth() + 1,
            d.getDate(),
            d.getHours(),
            d.getMinutes(),
            d.getSeconds(),
        )
        self.persistence.new_workout(workout_date=self.current_workout_date)
        self.persistence.save()
        self._dom_show_workout()

    def on_workout_click(self, event) -> None:
        target = event.target.closest(".workout-item")
        if target:
            self.current_workout_date = str(target.getAttribute("workout-date"))
            self._dom_show_workout()

    def _dom_show_workout(self) -> None:
        assert self.current_workout_date != ""

        self._dom_show_view("view-workout")
        document.getElementById("workout-date").textContent = self.current_workout_date

        container = document.getElementById("exercises-list")
        container.innerHTML = ""

        for exercise in self.persistence.who.exercises:
            done = self.persistence.workouts.get_workout_exercise(
                machine=exercise.machine, workout_date=self.current_workout_date
            ).done
            li = document.createElement("li")
            li.className = "exercise-item" + (" done" if done else "")
            li.setAttribute("data-key", exercise.machine)

            span_key = document.createElement("span")
            span_key.className = "exercise-key"
            span_key.textContent = exercise.machine

            span_name = document.createElement("span")
            span_name.className = "exercise-name"
            span_name.textContent = exercise.short

            li.appendChild(span_key)
            li.appendChild(span_name)
            if exercise.priority != "":
                img = document.createElement("img")
                img.src = f"./assets/{exercise.priority}"
                img.className = "priority-icon"
                img.alt = exercise.priority
                li.appendChild(img)
            container.appendChild(li)

    def on_exercise_click(self, event) -> None:
        target = event.target.closest(".exercise-item")
        if target:
            machine = str(target.getAttribute("data-key"))
            self.current_exercise = self.persistence.get_current_exercise(
                workout_date=self.current_workout_date,
                machine=machine,
            )
            self._dom_show_exercise()

    def _dom_show_exercise(self) -> None:
        self._dom_show_view("view-exercise")

        assert self.current_exercise is not None
        exercise = self.current_exercise.exercise

        workout_exercise = self.current_exercise.get_workout_exercise(
            persistence=self.persistence
        )

        document.getElementById("exercise-key").textContent = exercise.machine
        document.getElementById("exercise-short").textContent = exercise.short
        document.getElementById("exercise-comment").textContent = exercise.comment
        document.getElementById("exercise-weight").value = str(workout_exercise.weight)
        document.getElementById("exercise-set1").value = str(workout_exercise.set1)
        document.getElementById("exercise-set2").value = str(workout_exercise.set2)

        card = document.getElementById("exercise-detail-card")
        done = workout_exercise.done
        if done:
            card.classList.add("done")
        else:
            card.classList.remove("done")

        btn_done = document.getElementById("btn-done")
        SVG_LEFT = '<svg><use href="#arrow-left"/></svg>'
        SVG_RIGHT = '<svg><use href="#arrow-right"/></svg>'
        if done:
            btn_done.innerHTML = f"{SVG_LEFT} Undo Done"
        else:
            btn_done.innerHTML = f"Done {SVG_RIGHT}"

    def on_done_exercise(self, event=None) -> None:
        assert self.current_exercise is not None

        workout_exercise = self.current_exercise.get_workout_exercise(
            persistence=self.persistence
        )
        weight_val = str(document.getElementById("exercise-weight").value)
        if weight_val:
            workout_exercise.weight = float(weight_val)

        set1 = str(document.getElementById("exercise-set1").value)
        if set1:
            workout_exercise.set1 = int(set1)
        set2 = str(document.getElementById("exercise-set2").value)
        if set1:
            workout_exercise.set2 = int(set2)

        workout_exercise.done = not workout_exercise.done

        self.persistence.save()
        self._dom_show_workout()

    def on_show_json(self, event=None) -> None:
        assert self.current_workout_date != ""
        self._dom_show_view("view-json")
        document.getElementById(
            "json-content"
        ).value = self.persistence.workouts.persistent_text
        document.getElementById("json-error").textContent = ""

    def on_save_json(self, event=None) -> None:
        workout_text = str(document.getElementById("json-content").value)
        error_el = document.getElementById("json-error")
        try:
            workouts = application.Workouts.persistent_factory(
                workouts_text=workout_text
            )
        except ValueError as e:
            error_el.textContent = f"Invalid Python: {e}"
            return
        self.persistence.set_workouts(workouts=workouts)
        self.persistence.save()
        error_el.textContent = ""
        self._dom_show_workout()

    def on_back_from_json(self, event=None) -> None:
        self._dom_show_workout()

    def on_cancel_exercise(self, event=None) -> None:
        self._dom_show_workout()

    def on_delete_storage(self, event=None) -> None:
        self.current_workout_date = ""
        self.persistence.delete_storage()
        self.on_show_workouts()

    def on_delete_workout(self, event=None) -> None:
        self.persistence.delete_workout(workout_date=self.current_workout_date)
        self.on_show_workouts()


APP = FitnessApp()
