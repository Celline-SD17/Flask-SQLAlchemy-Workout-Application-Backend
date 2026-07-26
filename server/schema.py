from marshmallow import Schema, fields

class ExerciseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    category = fields.Str()
    equipment_needed = fields.Bool()


class WorkoutSchema(Schema):
    id = fields.Int()
    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.Str()


class WorkoutExerciseSchema(Schema):
    id = fields.Int()
    workout_id = fields.Int()
    exercise_id = fields.Int()
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema()
