# Task CRUD API

## Description

A simple RESTful CRUD API for managing tasks.
Built with Python and FastAPI.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Input validation
- Swagger UI documentation
- In-memory data storage

## Technologies

- Python
- FastAPI
- Uvicorn
- Pydantic

## Installation

1. Clone the repository
2. Create virtual environment
3. Install dependencies
4. Run the server

## Run

uvicorn main:app --reload

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | API information |
| GET | /health | Health check |
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get one task |
| POST | /tasks | Create task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |

## Swagger UI

http://localhost:8000/docs

[Swagger Screenshot]

## Testing

Example curl commands...

## Status Codes

200 - OK
201 - Created
204 - No Content
400 - Bad Request
404 - Not Found