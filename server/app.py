from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from datetime import date


from models import *
from schema import *

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
    return make_response(workouts_schema.dump(workouts), 200)


#Getting workout by ID
@app.route("/workouts/<int:id>")
def get_workout(id):
    workout = Workout.query.filter(Workout.id == id).first()
    if not workout:
        return make_response(
            {"error": "Workout not found"},
            404
        )
    return make_response(workout_schema.dump(workout), 200)


#Creating a workout
@app.route("/workouts", methods=["POST"])
def create_workout():
    json_data = request.get_json()
    try:
        data = workout_schema.load(json_data)
        workout = Workout(
            date=data["date"],
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes")
        )
        db.session.add(workout)
        db.session.commit()
        response_body = workout_schema.dump(workout)
        return make_response(response_body, 201)
    except ValidationError as err:
        return make_response(err.messages, 400)
    except ValueError as err:
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
    response_body = exercises_schema.dump(exercises)
    return make_response(response_body, 200)

#Get exercise by ID
@app.route("/exercises/<int:id>")
def get_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    response_body = exercise_schema.dump(exercise)
    return make_response(response_body, 200)

#Creating an exercise
@app.route("/exercises", methods=["POST"])
def create_exercise():
    json_data = request.get_json()
    try:
        data = exercise_schema.load(json_data)
        exercise = Exercise(
            name=data["name"],
            category=data["category"],
            equipment_needed=data["equipment_needed"]
        )
        db.session.add(exercise)
        db.session.commit()
        response_body = exercise_schema.dump(exercise)
        return make_response(response_body, 201)
    except ValidationError as err:
        return make_response(err.messages, 400)
    except ValueError as err:
        return make_response(
            {"error": str(err)},
            400
        )

    
#Deleting an exercise
@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
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
        data = workout_exercise_schema.load(json_data)
        workout_exercise = WorkoutExercises(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds")
        )
        db.session.add(workout_exercise)
        db.session.commit()
        response_body = workout_exercise_schema.dump(
            workout_exercise
        )
        return make_response(response_body, 201)
    except ValidationError as err:
        return make_response(err.messages, 400)
    except ValueError as err:
        return make_response(
            {"error": str(err)},
            400
        )

if __name__ == '__main__':
    app.run(port=5555, debug=True)