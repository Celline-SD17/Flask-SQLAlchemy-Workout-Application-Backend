#!/usr/bin/env python3
from random import randint, choice,sample
from datetime import timedelta
from faker import Faker
from app import app
from models import *

fake = Faker()
categories = ["Strength", "Cardio", "Flexibility", "Balance", "Mobility"]
exercise_names = [
    "Push Ups",
    "Squats",
    "Bench Press",
    "Deadlift",
    "Running",
    "Cycling",
    "Jump Rope",
    "Plank",
    "Burpees",
    "Lunges",
    "Pull Ups",
    "Shoulder Press",
    "Mountain Climbers",
    "Leg Press",
    "Crunches"
]

with app.app_context():
	#Deleting old data 
    print("Deleting old data...")
    WorkoutExercises.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    #Creating exercises 
    print("Creating exercises...")
    exercises = []
    selected_names = sample(exercise_names, 10)
    for name in selected_names:
        exercise = Exercise(
            name=name,
            category=choice(categories),
            equipment_needed=choice([True, False])
        )
        exercises.append(exercise)
    db.session.add_all(exercises)
    db.session.commit()
    #Creating workouts
    print("Creating workouts...")
    workouts = []
    for _ in range(5):
        workout = Workout(
            date=fake.date_between(
                start_date="-30d",
                end_date="today"
            ),
            duration_minutes=randint(20, 90),
            notes=fake.sentence()
        )
        workouts.append(workout)
    db.session.add_all(workouts)
    db. session.commit()

    #Linking workouts and exercises
    print("Linking workouts and exercises...")
    workout_exercises = []
    for workout in workouts:
        chosen_exercises = sample(exercises, randint(3,5))
        for exercise in chosen_exercises:
            if exercise.category == "Cardio":
                link = WorkoutExercises(
                    workout=workout,
                    exercise=exercise,
                    duration_seconds=randint(60, 900),
                    sets=None,
                    reps=None
                )
            else:
                link = WorkoutExercises(
                    workout=workout,
                    exercise=exercise,
                    sets=randint(2, 5),
                    reps=randint(8, 20),
                    duration_seconds=None
                )
            workout_exercises.append(link)
    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Database seeded successfully!")
    
 

