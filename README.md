# Workout Tracker API
## Description
- The Workout Tracker API is a RESTful backend application built with Flask that allows personal trainers to manage workouts and exercises. 
- The API supports creating, viewing, and deleting workouts and exercises, as well as assigning exercises to workouts with workout-specific details such as sets, reps, or duration.
- The application uses SQLAlchemy ORM for database management, Marshmallow for serialization and validation, and SQLite as the database. Model, schema, and database-level validations help ensure that only valid data is stored.
## Features
-  Create, view, and delete workouts.
-  Create, view, and delete exercises.
-  Add exercises to workouts.
-  Many-to-many relationship between workouts and exercises through a join table namely workout_exercises.
-  Model, schema, and database validations.
-  Seed database with sample data using Faker.
-  JSON responses for all API endpoints.
## Technologies Used
    * Python 3
    * Flask
    * Flask SQLAlchemy
    * Marshmallow
    * SQLite
    * Faker
## Installation Instructions
1. Clone my gitHub repsitory- ([[https://github.com/Celline-SD17/Flask-SQLAlchemy-Workout-Application-Backend]])
2. Navigate to the project directory: 
    * cd Flask-SQLAlchemy-Workout-Application-Backend
3. Install project dependencies:
    * pipenv install
4. Activate the virtual environment:
    * pipenv shell
5. Navigate to the server folder:
    * cd server
6. Initialize the database only for the first time:
    * flask db init
7. Generate a migration:
    * flask db migrate -m "Initial migration"
8. Apply the migration:
    *flask db upgrade head
9. Seed the database:
    python3 seed.py
## Running the Application
- Start the Flask development server:
    * use python3 app.py
- The application will be available at: ([[http://127.0.0.1:5555]])

## API Endpoints
### Workouts
```
Method  	Endpoint	        Description
GET	        /workouts	        Retrieve all workouts
GET	        /workouts/<id>	    Retrieve a specific workout
POST	    /workouts	        Create a new workout
DELETE	    /workouts/<id>	    Delete a workout
```

### Example Requests:
- creating a workout:
    
    Post/Workouts
    
    Request Body:
    {
        "date": "2026-07-27",
        "duration_minutes": 60,
        "notes": "Upper body strength workout."
    }

    Example Response:
     {
        "id": 6,
        "date": "2026-07-27",
        "duration_minutes": 60,
        "notes": "Upper body strength workout.",
        "workout_exercises": []
    }



### Exercises
```
Method	    Endpoint	            Description
GET	        /exercises	            Retrieve all exercises
GET	        /exercises/<id>	        Retrieve a specific exercise
POST	    /exercises	            Create a new exercise
DELETE	    /exercises/<id>	        Delete an exercise
```

- Creating an Exercise
    POST /exercises


    Request Body:

    {
        "name": "Bench Press",
        "category": "Strength",
        "equipment_needed": true
    }

    - Example Response:

    {
        "id": 11,
        "name": "Bench Press",
        "category": "Strength",
        "equipment_needed": true,
        "workouts": []
    }

### Workout Exercises
```
Method	    Endpoint	                                                   
POST	    /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises   

This endpoint is used for adding an exercise to a workout, including sets, reps, or duration. 
```


## Database Models
### Exercise
    * id
    * name
    * category
    * equipment_needed
### Workout
    * id
    * date
    * duration_minutes
    * notes
### WorkoutExercises
    * id
    * workout_id
    * exercise_id
    * reps
    * sets
    * duration_seconds
## Validation
- This app includes validations at multiple levels:
### Database Constraints
    - Required fields cannot be null.
    - Exercise names must be unique.
### Model Validations
    - Exercise names must contain at least two characters.
    - Exercise category must be one of the allowed categories.
    - Workout duration must be greater than zero.
    - Sets, reps, and duration values must be positive.
### Schema Validations
    - Required request fields are validated before creating records.
    - Exercise categories are validated.
    - Workout duration must be greater than zero.
    - A workout exercise must include either:
        * both reps and sets, or duration_seconds
    - A workout exercise cannot include both duration_seconds and reps/sets simultaneously.
## Project Structure

```
Workout-Tracker-API/
│
├── .gitignore
├── README.md
├── Pipfile
├── Pipfile.lock
│
└── server/
    ├── app.py
    ├── models.py
    ├── schema.py
    ├── seed.py
    ├── instance/
    │   └── app.db
    └── migrations/
        ├── alembic.ini
        ├── env.py
        ├── README
        ├── script.py.mako
        └── versions/
            └── xxxxxxxxx_initial_migration.py
```

## Author
    - Developed as a Flask, SQLAlchemy, and Marshmallow backend API project.
### License
    - The project was developed for the fulfilment of educational requirements, but can be a useful tool for personal trainers to develop training programs..

