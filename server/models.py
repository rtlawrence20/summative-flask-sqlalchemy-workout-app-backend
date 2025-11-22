# server/models.py
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name must not be empty.")
        if len(value.strip()) < 3:
            raise ValueError("Exercise name must be at least 3 characters.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise category must not be empty.")
        return value.strip()

    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String, nullable=False, unique=True
    )  # unique exercise names constraint
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
        overlaps="workouts,exercises",
    )

    # many-to-many convenience relationship
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        overlaps="workout_exercises,exercise",
    )


class Workout(db.Model):

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None:
            raise ValueError("Workout duration is required.")
        if value <= 0:
            raise ValueError("Workout duration must be positive.")
        return value

    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # relationships
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
        overlaps="exercises,workouts",
    )

    # many-to-many convenience relationship
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        overlaps="workout_exercises,exercise",
    )

    # constraints
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="check_workout_duration_positive"),
    )


class WorkoutExercise(db.Model):

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be positive if provided.")
        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be positive if provided.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Duration (seconds) must be positive if provided.")
        return value

    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # relationships
    workout = db.relationship(
        "Workout", back_populates="workout_exercises", overlaps="exercises,workouts"
    )
    exercise = db.relationship(
        "Exercise", back_populates="workout_exercises", overlaps="workouts,exercises"
    )

    # constraints
    __table_args__ = (
        CheckConstraint("reps IS NULL OR reps >= 0", name="check_reps_non_negative"),
        CheckConstraint("sets IS NULL OR sets >= 0", name="check_sets_non_negative"),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds >= 0",
            name="check_duration_non_negative",
        ),
    )
