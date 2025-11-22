# server/app.py

from sqlalchemy.exc import IntegrityError
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from .models import db, Workout, Exercise, WorkoutExercise
from .schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init extensions
db.init_app(app)
migrate = Migrate(app, db)

# Schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)


# ------------------------
# Basic routes
# ------------------------
def not_found(message="Resource not found"):
    """Helper for 404 responses."""
    return jsonify({"message": message}), 404


@app.route("/")
def index():
    return jsonify({"message": "Workout API backend is running."}), 200


# ------------------------
# Workout routes
# ------------------------
@app.route("/workouts", methods=["GET"])
def get_workouts():
    """Get all workouts."""
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    """Get a single workout by ID."""
    workout = Workout.query.get(id)
    if not workout:
        return not_found("Workout not found")
    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    """Create a new workout."""
    json_data = request.get_json() or {}

    try:
        data = workout_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"message": "Invalid data", "errors": err.messages}), 400

    if isinstance(data, dict):
        workout = Workout(**data)
    else:
        workout = data

    db.session.add(workout)
    db.session.commit()

    return jsonify(workout_schema.dump(workout)), 201


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    """Delete a workout by ID."""
    workout = Workout.query.get(id)
    if not workout:
        return not_found("Workout not found")

    db.session.delete(workout)
    db.session.commit()

    return "", 204


# ------------------------
# Exercise routes
# ------------------------
@app.route("/exercises", methods=["GET"])
def get_exercises():
    """Get all exercises."""
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    """Get a single exercise by ID."""
    exercise = Exercise.query.get(id)
    if not exercise:
        return not_found("Exercise not found")

    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    """Create a new exercise."""
    json_data = request.get_json() or {}

    try:
        data = exercise_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"message": "Invalid data", "errors": err.messages}), 400

    if isinstance(data, dict):
        exercise = Exercise(**data)
    else:
        exercise = data

    db.session.add(exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return (
            jsonify(
                {
                    "message": "Exercise with this name already exists.",
                }
            ),
            400,
        )

    return jsonify(exercise_schema.dump(exercise)), 201


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    """Delete an exercise by ID."""
    exercise = Exercise.query.get(id)
    if not exercise:
        return not_found("Exercise not found")

    db.session.delete(exercise)
    db.session.commit()
    return "", 204


# ------------------------
# Join route (WorkoutExercise)
# ------------------------
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_workout_exercise(workout_id, exercise_id):
    """Create a WorkoutExercise join record."""
    workout = Workout.query.get(workout_id)
    if not workout:
        return not_found("Workout not found")

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return not_found("Exercise not found")

    json_data = request.get_json() or {}
    json_data["workout_id"] = workout_id
    json_data["exercise_id"] = exercise_id

    try:
        data = workout_exercise_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"message": "Invalid data", "errors": err.messages}), 400

    if isinstance(data, dict):
        join_record = WorkoutExercise(**data)
    else:
        join_record = data

    db.session.add(join_record)
    db.session.commit()

    return jsonify(workout_exercise_schema.dump(join_record)), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
