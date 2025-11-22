# tests/test_routes.py

import json
from datetime import date

from server.models import Workout, Exercise, WorkoutExercise, db


def test_get_workouts(client, app):
    resp = client.get("/workouts")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)


def test_get_workout_not_found(client):
    resp = client.get("/workouts/99999")
    assert resp.status_code == 404
    body = resp.get_json()
    assert "message" in body


def test_create_workout_valid(client, app):
    payload = {
        "date": "2025-01-10",
        "duration_minutes": 45,
        "notes": "API test workout",
    }
    resp = client.post(
        "/workouts",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["duration_minutes"] == 45
    assert "id" in data


def test_delete_workout(client, app):
    # create a workout directly
    with app.app_context():
        w = Workout(date=date(2025, 1, 15), duration_minutes=30, notes="To delete")
        db.session.add(w)
        db.session.commit()
        wid = w.id

    resp = client.delete(f"/workouts/{wid}")
    assert resp.status_code in (200, 204)

    with app.app_context():
        assert Workout.query.get(wid) is None


def test_get_exercises(client):
    resp = client.get("/exercises")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)


def test_create_exercise_valid(client, app):
    payload = {
        "name": "API Curl",
        "category": "Strength",
        "equipment_needed": True,
    }
    resp = client.post(
        "/exercises",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "API Curl"


def test_create_exercise_duplicate_name_fails(client, app):
    payload = {
        "name": "Duplicate Squat",
        "category": "Strength",
        "equipment_needed": False,
    }
    # First time should succeed
    resp1 = client.post(
        "/exercises",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp1.status_code == 201

    # Second time should fail with 400 due to unique constraint
    resp2 = client.post(
        "/exercises",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp2.status_code == 400
    body = resp2.get_json()
    assert "message" in body


def test_join_route_adds_workout_exercise(client, app):
    # create a workout + exercise first if not present
    with app.app_context():
        w = Workout(date=date(2025, 2, 1), duration_minutes=20, notes="Join test")
        e = Exercise(
            name="Join Test Exercise", category="Cardio", equipment_needed=False
        )
        db.session.add_all([w, e])
        db.session.commit()
        wid, eid = w.id, e.id

    payload = {"reps": 10, "sets": 3}
    resp = client.post(
        f"/workouts/{wid}/exercises/{eid}/workout_exercises",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["workout_id"] == wid
    assert data["exercise_id"] == eid
