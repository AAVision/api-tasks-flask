from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/flask_api"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class PrioritiesModel(db.Model):
    __tablename__ = "priority"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    tasks = db.relationship("TasksModel", backref="priority")


class TasksModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.Text())
    completed = db.Column(db.Boolean())
    priority_id = db.Column(db.Integer, db.ForeignKey("priority.id"), nullable=False)


# To check the available priorities
@app.route("/priorities", methods=["GET"])
def get_priorities():
    priorities = PrioritiesModel.query.order_by(PrioritiesModel.id.asc()).all()
    results = [
        {
            "id": p.id,
            "name": p.name,
        }
        for p in priorities
    ]
    return results


## block of Getting and adding a task
@app.route("/tasks", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        priority = request.args.get("priority")

        tasks = (
            TasksModel.query.join(PrioritiesModel).order_by(TasksModel.id.desc()).all()
        )

        # if priority.isdigit():
        #     tasks = tasks.filter(tasks.priority_id == int(priority))
            

        results = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority.name,
            }
            for task in tasks
        ]
        return {"count": len(tasks), "tasks": results, "priority": priority}
    elif request.method == "POST":
        if request.is_json:
            data = request.get_json()
            new_task = TasksModel(
                title=data["title"],
                description=data["description"],
                completed=data["completed"],
                priority_id=data["priority_id"],
            )
            db.session.add(new_task)
            db.session.commit()
            return {"message": f"task {new_task.title} was added successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        return {"error": "Invalid request!"}


## block of Getting,Updating and Deleting a task
@app.route("/tasks/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = TasksModel().query.get_or_404(task_id)

    if request.method == "GET":
        response = {
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority.name,
        }
        return response
    
    elif request.method == "PUT" and request.is_json:
        data = request.get_json()
        task.title = data["title"]
        task.description = data["description"]
        task.completed = data["completed"]
        task.priority_id = data["priority_id"]
        db.session.commit()
        return {"message": f"task {task.title} was updated successfully."}
    
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {"message": f"task {task.title} was deleted successfully!"}
    
    else:
        return {"error": "Invalid request!"}
