from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3

DATABASE = "tasks.db"


def init_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Create tasks table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    # Check whether the table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    # Insert example tasks only if the table is empty
    if count == 0:
        cursor.executemany("""
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
        """, [
            ("Learn Python", False),
            ("Build CRUD API", False),
            ("Connect SQLite database", False)
        ])

    connection.commit()
    connection.close()


init_database()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None    

app = FastAPI()



@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return dict(row)

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """,
        (task.title, False)
    )

    task_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "id": task_id,
        "title": task.title,
        "done": False
    }

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):

    # Find the task
    for task in tasks:

        if task["id"] == task_id:

            # Check empty body
            if task_update.title is None and task_update.done is None:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Update body cannot be empty"}
                )

            # Update title
            if task_update.title is not None:

                if not task_update.title.strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )

                task["title"] = task_update.title

            # Update done
            if task_update.done is not None:
                task["done"] = task_update.done

            return task

    # Task not found
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )    

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    # Find the task
    for index, task in enumerate(tasks):

        if task["id"] == task_id:

            # Delete task
            tasks.pop(index)

            # 204 means no response body
            return None

    # Task not found
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )
