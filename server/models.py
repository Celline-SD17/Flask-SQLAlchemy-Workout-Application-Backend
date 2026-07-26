from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()


#Exercise Model
class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed=db.Column(db.Boolean, nullable=False)
    workout_exercises = db.relationship("WorkoutExercises", back_populates="exercise", cascade ="all, delete-orphan")
    workouts = db.relationship("Workout", secondary="workout_exercises", back_populates="exercises", viewonly=True)

    #Validating name
    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Exercise name is required")
        if len(value) < 2:
            raise ValueError("Exercise name must be at least 2 characters")
        return value    

    #Validating Category
    @validates("category")
    def validate_category(self, key, value):
        allowed = ["Strength", "Cardio", "Flexibility", "Balance", "Mobility"]
        if value not in allowed:
            raise ValueError(f"Category must be one of {allowed}")
        return value

    def __repr__(self):
        return f"<Exercise {self.id}, {self.name}, {self.category}, {self.equipment_needed}>"


#Workout Model definition
class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes=db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    workout_exercises = db.relationship("WorkoutExercises", back_populates="workout", cascade="all, delete-orphan")
    exercises = db.relationship("Exercise", secondary='workout_exercises', back_populates="workouts", viewonly=True)

    #Validating duration-minutes
    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be greater than 0")
        return value
    
    def __repr__(self):
        return f"<Workout {self.id}, {self.date}, {self.duration_minutes}, {self.notes}>"

# WorkoutExercises(Join table)
class WorkoutExercises(db.Model):
    __tablename__ = "workout_exercises"
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")


    #Validating sets
    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value < 1:
            raise ValueError("Sets must be at least 1")
        return value

    #Validating reps
    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value < 1:
            raise ValueError("Reps must be at least 1")
        return value

    #Validating duration_seconds
    @validates("duration_seconds")
    def validate_duration(self, key, value):
        if value is not None and value < 1:
            raise ValueError("Duration must be positive")
        return value
    def __repr__(self):
        return f"<WorkoutExercise {self.id}, {self.reps}, {self.sets}, {self.duration_seconds}>"

    

