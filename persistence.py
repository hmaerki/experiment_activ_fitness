from __future__ import annotations
import dataclasses
import js

import application
import configuration
import copy

STORAGE_KEY_WORKOUTS = "activ_fitness_workouts"
STORAGE_KEY_WHO = "activ_fitness_who"


@dataclasses.dataclass
class CurrentExercise:
    workout_date: str
    exercise: application.Exercise
    workout_exercise: application.WorkoutExercise

    def __post_init__(self) -> None:
        assert isinstance(self.workout_date, str)
        assert isinstance(self.exercise, application.Exercise)
        assert isinstance(self.workout_exercise, application.WorkoutExercise)

    def get_workout_exercise(
        self,
        persistence: Persistence,
    ) -> application.WorkoutExercise:
        return persistence.workouts.get_workout_exercise(
            workout_date=self.workout_date,
            machine=self.exercise.machine,
        )


class Persistence:
    def __init__(self) -> None:
        self.workouts = application.Workouts()
        workouts_text = js.localStorage.getItem(STORAGE_KEY_WORKOUTS)
        if workouts_text:
            self.workouts = application.Workouts.persistent_factory(
                workouts_text=workouts_text
            )
        _who_key = js.localStorage.getItem(STORAGE_KEY_WHO)
        if _who_key:
            who_key = str(_who_key)
        else:
            who_key = configuration.WHO_HANS.key
        self.who = configuration.DICT_WHO[who_key]

    def get_current_exercise(self, workout_date: str, machine: str) -> CurrentExercise:
        return CurrentExercise(
            workout_date=workout_date,
            exercise=self.who.get_exercise(machine=machine),
            workout_exercise=self.workouts.get_workout_exercise(
                workout_date=workout_date, machine=machine
            ),
        )

    def set_workouts(self, workouts: application.Workouts) -> None:
        application.Who.validate_workouts(workouts=workouts)
        self.workouts = workouts

    def new_workout(self, workout_date: str) -> None:
        assert isinstance(workout_date, str)
        self.workouts.append(
            application.Workout(
                workout_date=workout_date,
                exercises=copy.deepcopy(self.who.workout_template),
            )
        )

    def save(self) -> None:
        js.localStorage.setItem(STORAGE_KEY_WORKOUTS, self.workouts.persistent_text)

    def delete_workout(self, workout_date: str) -> None:
        if workout_date in self.dict_workouts:
            del self.dict_workouts[workout_date]
            self.save()

    def delete_storage(self) -> None:
        js.localStorage.removeItem(STORAGE_KEY_WORKOUTS)
        js.localStorage.removeItem(STORAGE_KEY_WHO)
        self.dict_workouts = {}

    def toggle_who(self) -> None:
        self.who = configuration.WHO_OTHER[self.who.key]
        js.localStorage.setItem(STORAGE_KEY_WHO, self.who.key)
