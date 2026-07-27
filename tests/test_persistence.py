import importlib
import sys
import types

import application


class FakeStorage:
    def __init__(self) -> None:
        self.items: dict[str, str] = {}

    def getItem(self, key: str) -> str | None:
        return self.items.get(key)

    def setItem(self, key: str, value: str) -> None:
        self.items[key] = value

    def removeItem(self, key: str) -> None:
        self.items.pop(key, None)


def test_new_workout_uses_last_workout_values(monkeypatch) -> None:
    fake_js = types.SimpleNamespace(localStorage=FakeStorage())
    monkeypatch.setitem(sys.modules, "js", fake_js)
    sys.modules.pop("persistence", None)

    persistence_module = importlib.import_module("persistence")
    persistence = persistence_module.Persistence()

    previous_workout = application.Workout(
        workout_date="2026-07-27",
        exercises=application.WorkoutExercises(
            [
                application.WorkoutExercise(
                    machine="D1/D4",
                    weight=31.0,
                    set1=12,
                    set2=13,
                    done=True,
                )
            ]
        ),
    )
    persistence.workouts = application.Workouts([previous_workout])

    persistence.new_workout("2026-07-28")

    new_workout = persistence.workouts.get_workout("2026-07-28")
    exercise = new_workout.exercises.get_exercise("D1/D4")

    assert exercise.weight == 31.0
    assert exercise.set1 == 12
    assert exercise.set2 == 13
    assert exercise.done is False
