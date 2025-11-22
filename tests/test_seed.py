# tests/test_seed.py

from server.models import Exercise, Workout, WorkoutExercise
from server.seed import seed_data


def test_seed_creates_data(app):
    """
    Basic check that seed_data() populates all three tables.
    Note: conftest already calls seed_data() once at session start.
    Here we call it again to ensure it clears and repopulates.
    """
    with app.app_context():
        seed_data()

        assert Exercise.query.count() >= 1
        assert Workout.query.count() >= 1
        assert WorkoutExercise.query.count() >= 1
