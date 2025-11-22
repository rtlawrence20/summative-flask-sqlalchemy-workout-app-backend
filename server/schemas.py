# server/schemas.py

from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Exercise, Workout, WorkoutExercise, db


# ---------------------------
# Exercise Schema
# ---------------------------
class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        include_fk = True
        load_instance = True
        sqla_session = db.session

    # Extra schema-level validation
    name = fields.String(required=True, validate=validate.Length(min=3))
    category = fields.String(required=True)


# ---------------------------
# WorkoutExercise Schema
# ---------------------------
class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        include_fk = True
        load_instance = True
        sqla_session = db.session

    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)

    @validates_schema
    def validate_at_least_one_field(self, data, **kwargs):
        """
        WorkoutExercise must have at least one of:
        - reps
        - sets
        - duration_seconds
        """
        if not any([data.get("reps"), data.get("sets"), data.get("duration_seconds")]):
            raise ValidationError(
                "WorkoutExercise requires reps, sets, or duration_seconds."
            )


# ---------------------------
# Workout Schema
# ---------------------------
class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        include_fk = True
        load_instance = True
        sqla_session = db.session

    # Nested relationship (READ ONLY)
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema), dump_only=True
    )
    exercises = fields.List(fields.Nested(ExerciseSchema), dump_only=True)

    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1))
