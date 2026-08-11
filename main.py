from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None    

app = FastAPI()

tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
    {"id": 2, "title": "Build API", "done": False},
    {"id": 3, "title": "Complete assignment", "done": True}
]

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
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    new_id = max([task["id"] for task in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task

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
