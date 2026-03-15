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
        v = eval(workouts_text)
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


FACTOR_TWO_MACHINES = "priority_snail.png"
FACTOR_DOUBLE_EXERCISE = "priority_emergency.png"

WHO_HANS = Who(
    key="hans",
    name="Hans",
    image="hans_im_glueck.svg",
    exercises=[
        Exercise(
            "F1",
            "Shoulder Press",
            "Technogym, Sitz 6",
        ),
        Exercise(
            "D1/D4",
            "Chest Press",
            "Nautilus, Sitz 7, Rücken 2",
            FACTOR_DOUBLE_EXERCISE,
        ),
        Exercise(
            "B7/D2",
            "Butterfly",
            "Nautilus, Fuss 4, Rücken 2",
            FACTOR_DOUBLE_EXERCISE,
        ),
        Exercise(
            "B5",
            "Lat Pull",
            "Technogym, Sitz 6",
        ),
        Exercise(
            "B4",
            "Cable Row Close",
            "Technogym",
        ),
        Exercise(
            "C3",
            "Torso Rotation sitting",
            "Nautilus ROM 80",
            FACTOR_DOUBLE_EXERCISE,
        ),
        Exercise(
            "C1",
            "Abdominal Crunch",
            "Nautilus, Sitz 6",
        ),
        Exercise(
            "B3",
            "Back Extension",
            "Technogym, Rücken 4, ROM 2",
            FACTOR_TWO_MACHINES,
        ),
        Exercise(
            "A5",
            "Leg Curls",
            "Technogym, Sitz 6, Fuss 5, ROM 2",
            FACTOR_TWO_MACHINES,
        ),
        Exercise(
            "A2",
            "Leg Press",
            "Sitz 4, Fuss 1",
            FACTOR_TWO_MACHINES,
        ),
    ],
    workout_template=WorkoutExercises(
        [
            WorkoutExercise(machine="D1/D4", weight=30.0),
            WorkoutExercise(machine="B7/D2", weight=23.0),
            WorkoutExercise(machine="B5", weight=40.0),
            WorkoutExercise(machine="F1", weight=15.0),
            WorkoutExercise(machine="B4", weight=20.0),
            WorkoutExercise(machine="C3", weight=36.0),
            WorkoutExercise(machine="C1", weight=30.0),
            WorkoutExercise(machine="B3", weight=35.0),
            WorkoutExercise(machine="A5", weight=35.0),
            WorkoutExercise(machine="A2", weight=60.0),
        ]
    ),
)
WHO_SANDRA = Who(
    key="sandra",
    name="Sandra",
    image="sandra_mit_hund.svg",
    exercises=[
        Exercise(
            "H2",
            "Trizepsstrecken",
            "Sitz 4, Rücken 4",
        ),
        Exercise(
            "F1",
            "Schulterdrücken",
            "Technogym, Sitz 4",
        ),
        Exercise(
            "E1",
            "ROM 1",
            "Abduktor",
        ),
        Exercise(
            "E2",
            "ROM 5",
            "Adduktor",
        ),
        Exercise(
            "D2",
            "Butterfly gebeugte Arme",
            "Technogym, Sitz 4",
        ),
        Exercise(
            "B5",
            "Lat Zug",
            "Technogym, Sitz 4",
        ),
        Exercise(
            "Mitte1",
            "Kurzhantel 45 Bank Seitenneigen",
            "Höhe 4",
            FACTOR_DOUBLE_EXERCISE,
        ),
        Exercise(
            "Mitte2",
            "45 Bank Rückenstrecken mit Gewicht",
            "Höhe 2",
            FACTOR_DOUBLE_EXERCISE,
        ),
        Exercise(
            "A5",
            "Beinbeuger",
            "Technogym, Sitz 2, Fuss 1, ROM 2",
            FACTOR_TWO_MACHINES,
        ),
        Exercise(
            "C1",
            "Bauch Crunch",
            "Nautilus, Sitz 3",
        ),
        Exercise(
            "A2",
            "Beinpresse",
            "Sitz 1, Fuss 3",
            FACTOR_TWO_MACHINES,
        ),
    ],
    workout_template=WorkoutExercises(
        [
            WorkoutExercise(machine="D2", weight=12.5, set1=18, set2=18),
            WorkoutExercise(machine="F1", weight=7.5, set1=15, set2=10),
            WorkoutExercise(machine="E1", weight=54.5, set1=16, set2=15),
            WorkoutExercise(machine="E2", weight=38.3, set1=18, set2=15),
            WorkoutExercise(machine="B5", weight=27.5, set1=18, set2=15),
            WorkoutExercise(machine="H2", weight=9.0, set1=18, set2=13),
            WorkoutExercise(machine="Mitte1", weight=3.0, set1=17, set2=17),
            WorkoutExercise(machine="Mitte2", weight=3.0, set1=16, set2=16),
            WorkoutExercise(machine="C1", weight=30.0, set1=18, set2=18),
            WorkoutExercise(machine="A5", weight=17.5, set1=18, set2=18),
            WorkoutExercise(machine="A2", weight=40.0, set1=18, set2=18),
        ]
    ),
)

LIST_WHO = (WHO_HANS, WHO_SANDRA)
WHO_OTHER = {WHO_HANS.key: WHO_SANDRA, WHO_SANDRA.key: WHO_HANS}
DICT_WHO = {who.key: who for who in LIST_WHO}

for who in LIST_WHO:
    who.validate()
