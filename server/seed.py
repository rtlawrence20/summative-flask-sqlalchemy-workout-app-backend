# server/seed.py

from datetime import date
from .app import app
from .models import db, Exercise, Workout, WorkoutExercise


def seed_data():
    print("Seeding database...")

    with app.app_context():
        # Clear tables in order (junction table first)
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()

        # --- Exercises ---
        exercises = [
            Exercise(name="Push-Up", category="Strength", equipment_needed=False),
            Exercise(name="Squat", category="Strength", equipment_needed=False),
            Exercise(name="Bench Press", category="Strength", equipment_needed=True),
            Exercise(name="Running", category="Cardio", equipment_needed=False),
            Exercise(name="Cycling", category="Cardio", equipment_needed=True),
        ]

        db.session.add_all(exercises)
        db.session.commit()

        # --- Workouts ---
        workouts = [
            Workout(date=date(2025, 1, 1), duration_minutes=45, notes="Leg day"),
            Workout(
                date=date(2025, 1, 2), duration_minutes=30, notes="Chest and triceps"
            ),
            Workout(date=date(2025, 1, 3), duration_minutes=60, notes="Cardio session"),
        ]

        db.session.add_all(workouts)
        db.session.commit()

        # --- WorkoutExercises (join table) ---
        join_records = [
            WorkoutExercise(
                workout_id=workouts[0].id, exercise_id=exercises[1].id, reps=12, sets=4
            ),
            WorkoutExercise(
                workout_id=workouts[1].id, exercise_id=exercises[2].id, reps=8, sets=3
            ),
            WorkoutExercise(
                workout_id=workouts[2].id,
                exercise_id=exercises[3].id,
                duration_seconds=1800,
            ),
        ]

        db.session.add_all(join_records)
        db.session.commit()

        print("Seed complete.")


if __name__ == "__main__":
    seed_data()
