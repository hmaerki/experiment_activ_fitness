# from __future__ import annotations


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
    WORKOUT_KEYS = ("done", "weight", "set1", "set2")
    WORKOUT_DEFAULT_VALUES: dict[str, float | int | bool] = {
        "weight": 40.0,
        "set1": 15,
        "set2": 15,
        "done": False,
    }

    def __init__(
        self,
        key: str,
        name: str,
        image: str,
        exercises: list[Exercise],
        workout_template: dict,
    ):
        self.key = key
        self.name = name
        self.image = image
        self.exercises = exercises
        self.workout_template = workout_template

    def validate(self) -> None:
        Who.validate_workout(self.workout_template)

    @staticmethod
    def validate_workout(
        dict_workout: dict[str, dict[str, float | int | bool]],
    ) -> None:
        for key, workout_exercise in dict_workout.items():
            assert isinstance(key, str)
            Who.validate_workout_exercise(workout_exercise=workout_exercise)

    @staticmethod
    def validate_workout_exercise(
        workout_exercise: dict[str, float | int | bool],
    ) -> None:
        for key, value in workout_exercise.items():
            assert key in Who.WORKOUT_KEYS
            assert isinstance(value, (float, int, bool)), value

    def get_exercise(self, machine: str) -> Exercise:
        for exercise in self.exercises:
            if exercise.machine == machine:
                return exercise
        raise ValueError(f"machine '{machine}' not found for '{self.key}'")

    def get_default_value(self, machine: str, key: str) -> float | int | bool:
        assert key in self.WORKOUT_KEYS
        dict_workout_exercise = self.workout_template[machine]
        default_value = self.WORKOUT_DEFAULT_VALUES[key]
        return dict_workout_exercise.get(key, default_value)


FACTOR_TWO_MACHINES = "priority_snail.png"
FACTOR_DOUBLE_EXERCISE = "priority_emergency.png"

WHO_HANS = Who(
    key="hans",
    name="Hans",
    image="hans_im_glueck.svg",
    exercises=[
        Exercise(
            "D1/D4",
            "Chest Press",
            "Nautilus, Sitz 7, Rücken 2",
            FACTOR_DOUBLE_EXERCISE,
        ),
        Exercise(
            "B2/B7",
            "Butterfly",
            "Nautilus, Rücken 2",
            FACTOR_DOUBLE_EXERCISE,
        ),
        Exercise(
            "B5",
            "Lat Pull",
            "Technogym, Sitz 6",
        ),
        Exercise(
            "F1",
            "Shoulder Press",
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
            "Technogym, Sitz 6, Fuss 6, ROM 2",
            FACTOR_TWO_MACHINES,
        ),
        Exercise(
            "A2",
            "Leg Press",
            "Sitz 4, Fuss 1",
            FACTOR_TWO_MACHINES,
        ),
    ],
    workout_template={
        "D1/D4": {"weight": 30.0},
        "B2/B7": {"weight": 23.0},
        "B5": {"weight": 40.0},
        "F1": {"weight": 15.0},
        "B4": {"weight": 20.0},
        "C3": {"weight": 36.0},
        "C1": {"weight": 30.0},
        "B3": {"weight": 35.0},
        "A5": {"weight": 35.0},
        "A2": {"weight": 60.0},
    },
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
    workout_template={
        "D2": {"weight": 12.5, "set1": 18, "set2": 18},
        "F1": {"weight": 7.5, "set1": 15, "set2": 10},
        "E1": {"weight": 54.5, "set1": 16, "set2": 15},
        "E2": {"weight": 38.3, "set1": 18, "set2": 15},
        "B5": {"weight": 27.5, "set1": 18, "set2": 15},
        "H2": {"weight": 9.0, "set1": 18, "set2": 13},
        "Mitte1": {"weight": 3.0, "set1": 17, "set2": 17},
        "Mitte2": {"weight": 3.0, "set1": 16, "set2": 16},
        "C1": {"weight": 30.0, "set1": 18, "set2": 18},
        "A5": {"weight": 17.5, "set1": 18, "set2": 18},
        "A2": {"weight": 40.0, "set1": 18, "set2": 18},
    },
)

LIST_WHO = (WHO_HANS, WHO_SANDRA)
WHO_OTHER = {WHO_HANS.key: WHO_SANDRA, WHO_SANDRA.key: WHO_HANS}
DICT_WHO = {who.key: who for who in LIST_WHO}

for who in LIST_WHO:
    who.validate()
