# tests/test_models.py

import pytest
from sqlalchemy.exc import IntegrityError

from server.models import db, Exercise, Workout, WorkoutExercise
from datetime import date


def test_exercise_name_required(db_session):
    # name is empty → should raise ValueError from @validates
    with pytest.raises(ValueError):
        ex = Exercise(name="  ", category="Strength", equipment_needed=False)
        db_session.add(ex)
        db_session.commit()


def test_workout_duration_must_be_positive(db_session):
    # duration_minutes <= 0 → should raise ValueError from @validates
    with pytest.raises(ValueError):
        w = Workout(date=date(2025, 1, 1), duration_minutes=0, notes="Bad")
        db_session.add(w)
        db_session.commit()


def test_exercise_name_unique_constraint(db_session):
    # First exercise with this name is OK
    ex1 = Exercise(name="Unique Squat", category="Strength", equipment_needed=False)
    db_session.add(ex1)
    db_session.commit()

    # Second exercise with same name → IntegrityError from unique constraint
    ex2 = Exercise(name="Unique Squat", category="Strength", equipment_needed=False)
    db_session.add(ex2)

    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_relationships_workout_exercise_many_to_many(db_session):
    w = Workout(date=date(2025, 1, 2), duration_minutes=30, notes="Test workout")
    e = Exercise(name="Test Push-Up", category="Strength", equipment_needed=False)

    db_session.add_all([w, e])
    db_session.commit()

    we = WorkoutExercise(workout_id=w.id, exercise_id=e.id, reps=10, sets=3)
    db_session.add(we)
    db_session.commit()

    # Reload to be explicit
    w2 = Workout.query.get(w.id)
    e2 = Exercise.query.get(e.id)

    assert len(w2.exercises) == 1
    assert w2.exercises[0].id == e.id

    assert len(e2.workouts) == 1
    assert e2.workouts[0].id == w.id

    assert len(w2.workout_exercises) == 1
    assert len(e2.workout_exercises) == 1
