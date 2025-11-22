# tests/test_schemas.py

import pytest
from marshmallow import ValidationError

from server.schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema


exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()


def test_exercise_schema_rejects_short_name():
    data = {"name": "Pu", "category": "Strength", "equipment_needed": False}
    with pytest.raises(ValidationError):
        exercise_schema.load(data)


def test_workout_schema_rejects_non_positive_duration():
    data = {
        "date": "2025-01-01",
        "duration_minutes": 0,
        "notes": "Bad duration",
    }
    with pytest.raises(ValidationError):
        workout_schema.load(data)


def test_workout_exercise_schema_requires_one_field():
    data = {
        "workout_id": 1,
        "exercise_id": 1,
        "reps": None,
        "sets": None,
        "duration_seconds": None,
    }
    with pytest.raises(ValidationError):
        workout_exercise_schema.load(data)
