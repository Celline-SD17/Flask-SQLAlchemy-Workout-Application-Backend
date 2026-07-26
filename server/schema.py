from marshmallow import (Schema, fields, validates, validates_schema, ValidationError)

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)
    workouts = fields.Nested("WorkoutSchema", many=True, exclude=("workout_exercises",), dump_only=True)

    @validates("name")
    def validate_name(self, value):
        if not value or len(value.strip()) < 2:
            raise ValidationError(
                "Exercise name must be at least 2 characters."
            )

    @validates("category")
    def validate_category(self, value):

        allowed = [
            "Strength",
            "Cardio",
            "Flexibility",
            "Balance",
            "Mobility"
        ]

        if value not in allowed:
            raise ValidationError(
                "Invalid exercise category."
            )

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.Nested(
        "WorkoutExerciseSchema",
        many=True,
        dump_only=True
    )

    @validates("duration_minutes")
    def validate_duration(self, value):

        if value <= 0:
            raise ValidationError(
                "Workout duration must be greater than zero."
            )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    exercise = fields.Nested(
        "ExerciseSchema",
        dump_only=True,
        exclude=("workouts",)
    )

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value < 1:
            raise ValidationError(
                "Sets must be at least 1."
            )
    @validates("reps")
    def validate_reps(self, value):

        if value is not None and value < 1:
            raise ValidationError(
                "Reps must be at least 1."
            )

    @validates("duration_seconds")
    def validate_duration(self, value):
        if value is not None and value < 1:
            raise ValidationError(
                "Duration must be greater than zero."
            )
    @validates_schema
    def validate_workout_data(self, data, **kwargs):
        reps = data.get("reps")
        sets = data.get("sets")
        duration = data.get("duration_seconds")
        if duration is None and (reps is None or sets is None):
            raise ValidationError(
                "Provide either duration_seconds or both reps and sets."
            )
        if duration is not None and (reps is not None or sets is not None):
            raise ValidationError(
                "Use either duration_seconds OR reps and sets, not both."
            )




exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
