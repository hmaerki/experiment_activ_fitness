from __future__ import annotations
import application


FACTOR_TWO_MACHINES = "priority_snail.png"
FACTOR_DOUBLE_EXERCISE = "priority_emergency.png"

WHO_HANS = application.Who(
    key="hans",
    name="Hans",
    image="hans_im_glueck.svg",
    exercises=[
        application.Exercise(
            "F1",
            "Shoulder Press",
            "Technogym, Sitz 6",
        ),
        application.Exercise(
            "D1/D4",
            "Chest Press",
            "Nautilus, Sitz 7, Rücken 2",
            FACTOR_DOUBLE_EXERCISE,
        ),
        application.Exercise(
            "B7/D2",
            "Butterfly",
            "Nautilus, Fuss 4, Rücken 2",
            FACTOR_DOUBLE_EXERCISE,
        ),
        application.Exercise(
            "B5",
            "Lat Pull",
            "Technogym, Sitz 6",
        ),
        application.Exercise(
            "B4",
            "Cable Row Close",
            "Technogym",
        ),
        application.Exercise(
            "C3",
            "Torso Rotation sitting",
            "Nautilus ROM 80",
            FACTOR_DOUBLE_EXERCISE,
        ),
        application.Exercise(
            "C1",
            "Abdominal Crunch",
            "Nautilus, Sitz 6",
        ),
        application.Exercise(
            "B3",
            "Back Extension",
            "Technogym, Rücken 4, ROM 2",
            FACTOR_TWO_MACHINES,
        ),
        application.Exercise(
            "A5",
            "Leg Curls",
            "Technogym, Sitz 6, Fuss 5, ROM 2",
            FACTOR_TWO_MACHINES,
        ),
        application.Exercise(
            "A2",
            "Leg Press",
            "Sitz 4, Fuss 1",
            FACTOR_TWO_MACHINES,
        ),
    ],
    workout_template=application.WorkoutExercises(
        [
            application.WorkoutExercise(machine="D1/D4", weight=30.0),
            application.WorkoutExercise(machine="B7/D2", weight=23.0),
            application.WorkoutExercise(machine="B5", weight=40.0),
            application.WorkoutExercise(machine="F1", weight=15.0),
            application.WorkoutExercise(machine="B4", weight=20.0),
            application.WorkoutExercise(machine="C3", weight=36.0),
            application.WorkoutExercise(machine="C1", weight=30.0),
            application.WorkoutExercise(machine="B3", weight=35.0),
            application.WorkoutExercise(machine="A5", weight=35.0),
            application.WorkoutExercise(machine="A2", weight=60.0),
        ]
    ),
)
WHO_SANDRA = application.Who(
    key="sandra",
    name="Sandra",
    image="sandra_mit_hund.svg",
    exercises=[
        application.Exercise(
            "H2",
            "Trizepsstrecken",
            "Sitz 4, Rücken 4",
        ),
        application.Exercise(
            "F1",
            "Schulterdrücken",
            "Technogym, Sitz 4",
        ),
        application.Exercise(
            "E1",
            "ROM 1",
            "Abduktor",
        ),
        application.Exercise(
            "E2",
            "ROM 5",
            "Adduktor",
        ),
        application.Exercise(
            "D2",
            "Butterfly gebeugte Arme",
            "Technogym, Sitz 4",
        ),
        application.Exercise(
            "B5",
            "Lat Zug",
            "Technogym, Sitz 4",
        ),
        application.Exercise(
            "Mitte1",
            "Kurzhantel 45 Bank Seitenneigen",
            "Höhe 4",
            FACTOR_DOUBLE_EXERCISE,
        ),
        application.Exercise(
            "Mitte2",
            "45 Bank Rückenstrecken mit Gewicht",
            "Höhe 2",
            FACTOR_DOUBLE_EXERCISE,
        ),
        application.Exercise(
            "A5",
            "Beinbeuger",
            "Technogym, Sitz 2, Fuss 1, ROM 2",
            FACTOR_TWO_MACHINES,
        ),
        application.Exercise(
            "C1",
            "Bauch Crunch",
            "Nautilus, Sitz 3",
        ),
        application.Exercise(
            "A2",
            "Beinpresse",
            "Sitz 1, Fuss 3",
            FACTOR_TWO_MACHINES,
        ),
    ],
    workout_template=application.WorkoutExercises(
        [
            application.WorkoutExercise(machine="D2", weight=12.5, set1=18, set2=18),
            application.WorkoutExercise(machine="F1", weight=7.5, set1=15, set2=10),
            application.WorkoutExercise(machine="E1", weight=54.5, set1=16, set2=15),
            application.WorkoutExercise(machine="E2", weight=38.3, set1=18, set2=15),
            application.WorkoutExercise(machine="B5", weight=27.5, set1=18, set2=15),
            application.WorkoutExercise(machine="H2", weight=9.0, set1=18, set2=13),
            application.WorkoutExercise(machine="Mitte1", weight=3.0, set1=17, set2=17),
            application.WorkoutExercise(machine="Mitte2", weight=3.0, set1=16, set2=16),
            application.WorkoutExercise(machine="C1", weight=30.0, set1=18, set2=18),
            application.WorkoutExercise(machine="A5", weight=17.5, set1=18, set2=18),
            application.WorkoutExercise(machine="A2", weight=40.0, set1=18, set2=18),
        ]
    ),
)

LIST_WHO = (WHO_HANS, WHO_SANDRA)
WHO_OTHER = {WHO_HANS.key: WHO_SANDRA, WHO_SANDRA.key: WHO_HANS}
DICT_WHO = {who.key: who for who in LIST_WHO}

for who in LIST_WHO:
    who.validate()
