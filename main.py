from fastapi import FastAPI, HTTPException
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

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    # Find the task in database
    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    )

    existing_task = cursor.fetchone()

    # Task not found
    if existing_task is None:
        connection.close()

        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    # Check empty body
    if task_update.title is None and task_update.done is None:
        connection.close()

        return JSONResponse(
            status_code=400,
            content={"error": "Update body cannot be empty"}
        )

    # Keep existing values
    current_title = existing_task[1]
    current_done = bool(existing_task[2])

    # Update title if provided
    if task_update.title is not None:

        if not task_update.title.strip():
            connection.close()

            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

        current_title = task_update.title

    # Update done if provided
    if task_update.done is not None:
        current_done = task_update.done

    # Update database
    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (current_title, current_done, task_id)
    )

    connection.commit()

    # Get updated task
    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    )

    updated_task = cursor.fetchone()

    connection.close()

    # Return updated task
    return {
        "id": updated_task[0],
        "title": updated_task[1],
        "done": bool(updated_task[2])
    }
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    )

    existing_task = cursor.fetchone()

    if existing_task is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return None
