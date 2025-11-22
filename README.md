# Flask SQLAlchemy Workout Application Backend

A Flask backend application for managing workouts, exercises, and
workout--exercise associations. This project uses SQLAlchemy,
Flask-Migrate, and Marshmallow for ORM, migrations, and schema
validation.

## 📌 Features

-   Full CRUD for **Workouts**
-   Full CRUD for **Exercises**
-   Ability to **add specific exercises** to a workout with
    reps/sets/duration
-   SQLite relational database with:
    -   1--many (Workout → WorkoutExercises)
    -   1--many (Exercise → WorkoutExercises)
    -   many--many convenience relationships
-   Model-level validations (`@validates`)
-   Schema-level validations (Marshmallow)
-   Table constraints (unique + check constraints)
-   Database seeding (`seed.py`)
-   Full API documentation

## 🛠️ Technologies

-   Python 3.12
-   Flask 2.2+
-   Flask-SQLAlchemy
-   Flask-Migrate
-   Marshmallow / Marshmallow-SQLAlchemy
-   SQLite (app.db)

## 🚀 Setup Instructions

### 1. Install dependencies

``` bash
pipenv install
pipenv shell
```

### 2. Environment variables

Inside the `server/` directory:

``` bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
export FLASK_DEBUG=1
```

### 3. Initialize database

``` bash
cd server
flask db upgrade
```

### 4. Seed the database

``` bash
python -m server.seed
```

## 📚 Database Models

### **Exercise**

  Field              Type      Notes
  ------------------ --------- ------------------
  id                 Integer   Primary key
  name               String    Required, unique
  category           String    Required
  equipment_needed   Boolean   Required

### **Workout**

  Field              Type      Notes
  ------------------ --------- -------------------
  id                 Integer   Primary key
  date               Date      Required
  duration_minutes   Integer   Positive required
  notes              Text      Optional

### **WorkoutExercise**

  Field              Type      Notes
  ------------------ --------- --------------------------------
  id                 Integer   Primary key
  workout_id         Integer   FK → Workout.id
  exercise_id        Integer   FK → Exercise.id
  reps               Integer   Optional, positive if provided
  sets               Integer   Optional, positive if provided
  duration_seconds   Integer   Optional, positive if provided

## 📡 API Endpoints

### 🏋️ Workouts

#### GET /workouts

Returns list of workouts.

#### GET /workouts/:id

Returns single workout.

#### POST /workouts

Body example:

``` json
{
  "date": "2025-01-01",
  "duration_minutes": 45,
  "notes": "Upper body"
}
```

#### DELETE /workouts/:id

Deletes a workout.

------------------------------------------------------------------------

### 🏃 Exercises

#### GET /exercises

Returns all exercises.

#### GET /exercises/:id

Returns a single exercise.

#### POST /exercises

``` json
{
  "name": "Push-Up",
  "category": "Strength",
  "equipment_needed": false
}
```

#### DELETE /exercises/:id

------------------------------------------------------------------------

### 🔗 WorkoutExercise

#### POST /workouts/:workout_id/exercises/:exercise_id/workout_exercises

Examples:

``` json
{ "reps": 10, "sets": 3 }
```

or:

``` json
{ "duration_seconds": 1800 }
```

------------------------------------------------------------------------

## 🌱 Seeding

``` bash
python -m server.seed
```

Verify:

``` bash
python -m server.check_seed
```

## 🧪 Developer Utilities

Ignored by Git:

-   prototest.py
-   check_seed.py

## ✔️ Status

Backend complete. All models, migrations, validations, seed data,
schemas, and endpoints fully implemented.
