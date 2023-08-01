# api-tasks-flask

## Introduction
This project is a simple CRUD task API implemented using Flask, SQL Alchemy, and PostgreSQL.

## Database
It consists of 2 tables: `tasks` and `priority` where in `priority` we have 3 types `High-Medium-Low` and there is a relation between the task and its priority.

## Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/AAVision/api-tasks-flask.git
    ```
2. Install all the dependencies from `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
3. Create your database in `pgadmin` and edit the configuration of `SQLALCHEMY_DATABASE_URI` in `app.py` file.
4. Run the migrations commands:
    ```bash
    flask db init 
    flask db migrate
    flask db upgrade
    ```
5. Run the application locally using:
    ```bash
    flask run
    ```
    and head to localhost:5000

## Endpoints
1. GET /tasks:
   ```bash
    GET localhost:5000/tasks
    {
        "count": 2, <-- for pagination
        "tasks": [
            {
                "completed": true,
                "description": "Implement DB",
                "id": 5,
                "priority": "Medium",
                "title": "database"
            },
            {
                "completed": true,
                "description": "Exam",
                "id": 3,
                "priority": "High",
                "title": "test 1"
            }
        ]
    }
   ```
2. POST /tasks:
   ```bash
    POST localhost:5000/tasks JSON 
    {
        "title":"Code",
        "description":"Add code",
        "completed":0,
        "priority_id":2
    }

    -->

    {
        "message": "task Code was added successfully."
    }
   ```
3. GET /tasks/{task_id}:
   ```bash
    GET localhost:5000/tasks/3
    {
        "completed": true,
        "description": "Exam",
        "id": 3,
        "priority": "High",
        "title": "test 1"
    }
   ```
4. PUT /tasks/{task_id}:
    ```bash
    PUT localhost:5000/tasks/3 JSON 
    {
        "title":"New Code",
        "description":"New code update",
        "completed":1,
        "priority_id":2
    }

    -->

    {
        "message": "task New Code was updated successfully."
    }
   ```
5. DELETE /tasks/{task_id}:
    ```bash
    DELETE localhost:5000/tasks/3
    {
        "message": "task New Code was deleted successfully."
    }
   ```
6. GET /priorities:
    ```bash
    [
        {
            "id": 1,
            "name": "High"
        },
        {
            "id": 2,
            "name": "Medium"
        },
        {
            "id": 3,
            "name": "Low"
        }
    ]
   ```