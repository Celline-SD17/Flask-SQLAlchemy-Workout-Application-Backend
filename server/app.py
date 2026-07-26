from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


#Home
@app.route("/")
def index():
    return "<h1>Workout Tracker API</h1>"


#Getting Workouts
@app.route("/workouts")
def get_workouts():
    workouts = Workout.query.all()
    response_body = []
    for workout in workouts:
        response_body.append({
            "id": workout.id,
            "date": workout.date.isoformat(),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        })

    return make_response(response_body)


#Getting workout by ID
@app.route("/workouts/<int:id>")
def get_workout(id):
    workout = Workout.query.filter(Workout.id == id).first()
    if not workout:
        return make_response(
            {"error": "Workout not found"},
            404
        )
    exercises = []
    for exercise in workout.exercises:
        exercises.append({
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        })
    response_body = {
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "exercises": exercises
    }
    return make_response(response_body)


#Creating a workout
@app.route("/workouts", methods=["POST"])
def create_workout():
    json_data = request.get_json()
    try:
        workout = Workout(
            date=json_data["date"],
            duration_minutes=json_data["duration_minutes"],
            notes=json_data.get("notes")
        )
        db.session.add(workout)
        db.session.commit()
        response_body = {
            "id": workout.id,
            "date": workout.date.isoformat(),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        }
        return make_response(response_body, 201)
    except Exception as err:
        return make_response(
            {"error": str(err)},
            400
        )


 #Deleting a Workout
@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.filter(
        Workout.id == id
    ).first()
    if not workout:
        return make_response(
            {"error": "Workout not found"},
            404
        )
    db.session.delete(workout)
    db.session.commit()
    return make_response({}, 204)


#Getting exercises
@app.route("/exercises")
def get_exercises():
    exercises = Exercise.query.all()
    response_body = []
    for exercise in exercises:
        response_body.append({
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        })
    return make_response(response_body)


#Get exercise by ID
@app.route("/exercises/<int:id>")
def get_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()
    if not exercise:
        return make_response(
            {"error": "Exercise not found"},
            404
        )
    workouts = []
    for workout in exercise.workouts:
        workouts.append({
            "id": workout.id,
            "date": workout.date.isoformat(),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        })
    response_body = {
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed,
        "workouts": workouts
    }
    return make_response(response_body)


#Creating an exercise
@app.route("/exercises", methods=["POST"])
def create_exercise():
    json_data = request.get_json()
    try:
        exercise = Exercise(
            name=json_data["name"],
            category=json_data["category"],
            equipment_needed=json_data["equipment_needed"]
        )
        db.session.add(exercise)
        db.session.commit()
        response_body = {
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        }
        return make_response(response_body, 201)
    except Exception as err:
        return make_response(
            {"error": str(err)},
            400
        )

    
#Deleting an exercise
@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()
    if not exercise:
        return make_response(
            {"error": "Exercise not found"}, 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response({}, 204)


#Adding an exercise to a workout
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.filter(Workout.id == workout_id).first()
    exercise = Exercise.query.filter(Exercise.id == exercise_id).first()
    if not workout or not exercise:
        return make_response(
            {"error": "Workout or Exercise not found"},
            404
        )
    json_data = request.get_json()
    try:
        workout_exercise = WorkoutExercises(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=json_data.get("reps"),
            sets=json_data.get("sets"),
            duration_seconds=json_data.get("duration_seconds")
        )
        db.session.add(workout_exercise)
        db.session.commit()
        response_body = {
            "id": workout_exercise.id,
            "workout_id": workout_exercise.workout_id,
            "exercise_id": workout_exercise.exercise_id,
            "reps": workout_exercise.reps,
            "sets": workout_exercise.sets,
            "duration_seconds": workout_exercise.duration_seconds
        }
        return make_response(response_body, 201)
    except Exception as err:
        return make_response(
            {"error": str(err)},
            400
        )

if __name__ == '__main__':
    app.run(port=5555, debug=True)