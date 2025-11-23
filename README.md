# Flask SQLAlchemy Workout Application Backend

A Flask backend application for managing workouts, exercises, and
workout/exercise relations. This project uses SQLAlchemy,
Flask-Migrate, and Marshmallow for ORM, migrations, and schema
validation.

## Features

-   Full CRUD for **Workouts**
-   Full CRUD for **Exercises**
-   Ability to **add specific exercises** to a workout with
    reps/sets/duration
-   SQLite relational database with:
    -   1 <-> many (Workout → WorkoutExercises)
    -   1 <-> many (Exercise → WorkoutExercises)
    -   many <-> many convenience relationships
-   Model-level validations (`@validates`)
-   Schema-level validations (Marshmallow)
-   Table constraints (unique + check constraints)
-   Database seeding (`seed.py`)
-   Full API documentation

## Requirements

-   Python 3.12
-   Flask 2.2+
-   Flask-SQLAlchemy
-   Flask-Migrate
-   Marshmallow / Marshmallow-SQLAlchemy
-   SQLite (app.db)

## Structure
```
├── Pipfile
├── Pipfile.lock
├── requirements.txt
├── README.md
├── instance
│   └── app.db
├── server
│   ├── __init__.py
│   ├── app.py
│   ├── migrations
│   │   ├── README
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── 8ced61c175e1_initial_schema_with_constraints.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── tests
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_routes.py
│   ├── test_schemas.py
│   └── test_seed.py
```

## Database Setup

This project uses SQLite.  
The active database file is always:

```
server/app.db
```

> **Note:** The database file is *not* committed to version control.  
> Anyone cloning the project will create their own DB using migrations + seed script.

---

## Setup Instructions

### 2. Set Flask environment variables

From project root:

```bash
export FLASK_APP=server.app
export FLASK_RUN_PORT=5555
```

### 3. Apply migrations

```bash
cd server
flask db upgrade
cd ..
```

### 4. Seed the database

```bash
python -m server.seed
```

### 5. Run the server

```bash
flask run
```

---

## Using sqlite-web to Inspect the Database

You can view database tables, columns, and rows using **sqlite-web**

### Open the database in sqlite-web

From the **project root**:

```bash
sqlite_web server/app.db
```

Then visit the printed URL, usually:

```
http://127.0.0.1:8080
```

You should see tables:

- `workouts`
- `exercises`
- `workout_exercises`
- `alembic_version`

---

## Database Models

### **Exercise**

| Field            | Type    | Notes            |
| ---------------- | ------- | ---------------- |
| id               | Integer | Primary key      |
| name             | String  | Required, unique |
| category         | String  | Required         |
| equipment_needed | Boolean | Required         |


### **Workout**

| Field            | Type    | Notes             |
| ---------------- | ------- | ----------------- |
| id               | Integer | Primary key       |
| date             | Date    | Required          |
| duration_minutes | Integer | Positive required |
| notes            | Text    | Optional          |


### **WorkoutExercise**

| Field            | Type    | Notes                          |
| ---------------- | ------- | ------------------------------ |
| id               | Integer | Primary key                    |
| workout_id       | Integer | FK → Workout.id                |
| exercise_id      | Integer | FK → Exercise.id               |
| reps             | Integer | Optional, positive if provided |
| sets             | Integer | Optional, positive if provided |
| duration_seconds | Integer | Optional, positive if provided |


## API Endpoints

### Workouts

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

### Exercises

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

### WorkoutExercise

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

## Running Tests

Run the full test suite with:

```bash
pytest
```