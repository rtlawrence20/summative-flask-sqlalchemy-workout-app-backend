# server/app.py

from flask import Flask, jsonify, request
from flask_migrate import Migrate

from .models import db, Workout, Exercise, WorkoutExercise
from .schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init extensions
db.init_app(app)
migrate = Migrate(app, db)


# ------------------------
# Basic routes
# ------------------------
@app.route("/")
def index():
    return jsonify({"message": "Workout API backend is running."}), 200


# ------------------------
# Workout routes
# ------------------------
@app.route("/workouts", methods=["GET"])
def get_workouts():
    # TODO: implement real logic w/ schemas
    return jsonify({"message": "GET /workouts not implemented yet"}), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    # TODO: implement real logic w/ schemas
    return jsonify({"message": f"GET /workouts/{id} not implemented yet"}), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    # TODO: implement creation w/ schema validation
    data = request.get_json() or {}
    return (
        jsonify(
            {
                "message": "POST /workouts not implemented yet",
                "received": data,
            }
        ),
        201,
    )


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    # TODO: implement real delete logic
    return jsonify({"message": f"DELETE /workouts/{id} not implemented yet"}), 200


# ------------------------
# Exercise routes
# ------------------------
@app.route("/exercises", methods=["GET"])
def get_exercises():
    # TODO: implement real logic w/ schemas
    return jsonify({"message": "GET /exercises not implemented yet"}), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    # TODO: implement real logic w/ schemas
    return jsonify({"message": f"GET /exercises/{id} not implemented yet"}), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    # TODO: implement creation w/ schema validation
    data = request.get_json() or {}
    return (
        jsonify(
            {
                "message": "POST /exercises not implemented yet",
                "received": data,
            }
        ),
        201,
    )


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    # TODO: implement real delete logic
    return jsonify({"message": f"DELETE /exercises/{id} not implemented yet"}), 200


# ------------------------
# Join route (WorkoutExercise)
# ------------------------
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_workout_exercise(workout_id, exercise_id):
    # TODO: implement creation of WorkoutExercise via schema
    data = request.get_json() or {}
    return (
        jsonify(
            {
                "message": "POST join workout/exercise not implemented yet",
                "workout_id": workout_id,
                "exercise_id": exercise_id,
                "received": data,
            }
        ),
        201,
    )


if __name__ == "__main__":
    app.run(port=5555, debug=True)
