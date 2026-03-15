from __future__ import annotations
import dataclasses


@dataclasses.dataclass
class WorkoutExercise:
    machine: str
    weight: float = 40.0
    set1: int = 15
    set2: int = 15
    done: bool = False

    def __post_init__(self) -> None:
        assert isinstance(self.machine, str)
        assert isinstance(self.weight, float)
        assert isinstance(self.set1, int)
        assert isinstance(self.set2, int)
        assert isinstance(self.done, bool)


class WorkoutExercises(list[WorkoutExercise]):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

    @property
    def progress_text(self) -> str:
        done_count = sum(1 for v in self if v.done)
        total_count = len(self)
        return f"{done_count}/{total_count} done"

    def get_exercise(self, machine: str) -> WorkoutExercise:
        for exercise in self:
            if exercise.machine == machine:
                return exercise
        raise ValueError(
            f"machine '{machine}' not found! {','.join(e.machine for e in self)}"
        )


@dataclasses.dataclass
class Workout:
    workout_date: str
    exercises: WorkoutExercises


class Workouts(list[Workout]):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

    def get_workout(self, workout_date: str, remove_done: bool = False) -> Workout:
        for workout in self:
            if workout.workout_date == workout_date:
                if remove_done:
                    for exercise in workout.exercises:
                        exercise.done = False
                return workout
        raise ValueError(f"workoutdate '{workout_date} not found!")

    def get_workout_exercise(self, workout_date: str, machine: str) -> WorkoutExercise:
        return self.get_workout(workout_date=workout_date).exercises.get_exercise(
            machine=machine
        )

    @property
    def has_workouts(self) -> bool:
        return len(self) > 0

    @property
    def persistent_text(self) -> str:
        return repr(self)

    @staticmethod
    def persistent_factory(workouts_text: str) -> Workouts:
        try:
            v = eval(workouts_text)
        except Exception:
            return Workouts()
        assert isinstance(v, Workouts)
        return v

    @property
    def workout_dates(self) -> list[str]:
        return sorted({w.workout_date for w in self}, reverse=True)

    def get_progress(self, workout_date: str) -> str:
        workout = self.get_workout(workout_date=workout_date)
        return workout.exercises.progress_text


class Exercise:
    def __init__(
        self,
        machine: str,
        short: str,
        comment: str,
        priority: str = "",
    ):
        self.machine = machine
        self.short = short
        self.comment = comment
        self.priority = priority


class Who:
    def __init__(
        self,
        key: str,
        name: str,
        image: str,
        exercises: list[Exercise],
        workout_template: WorkoutExercises,
    ):
        self.key = key
        self.name = name
        self.image = image
        self.exercises = exercises
        self.workout_template = workout_template

    def validate(self) -> None:
        Who.validate_workout_exercisses(self.workout_template)
        for workout_exercise in self.workout_template:
            self.get_exercise(workout_exercise.machine)

    @staticmethod
    def validate_workouts(workouts: Workouts) -> None:
        for workout in workouts:
            assert isinstance(workout, Workout)
            Who.validate_workout_exercisses(workout_exercises=workout.exercises)

    @staticmethod
    def validate_workout_exercisses(workout_exercises: WorkoutExercises) -> None:
        for workout_exercise in workout_exercises:
            assert isinstance(workout_exercise, WorkoutExercise)

    def get_exercise(self, machine: str) -> Exercise:
        for exercise in self.exercises:
            if exercise.machine == machine:
                return exercise
        raise ValueError(f"machine '{machine}' not found for '{self.key}'")
