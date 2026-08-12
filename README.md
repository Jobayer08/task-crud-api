# Task CRUD API

## Description

A simple RESTful CRUD API for managing tasks.

Built with Python and FastAPI.

This project uses SQLite for persistent data storage. Tasks are stored in a
SQLite database instead of in-memory data, so the data remains available
after restarting the server.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Input validation
- SQLite database storage
- Persistent data across server restarts
- Automatic database and table creation
- Swagger UI documentation

## Technologies

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLite

## Database

This project uses SQLite for persistent data storage.

SQLite was chosen because it is lightweight, simple to use, and does not
require a separate database server.

The database file is:

```text
tasks.db