# To-Do List Project — FastAPI + HTML/CSS/JS

## Project Structure

```
todo_project/
├── backend/
│   ├── main.py           ← All API routes (GET, POST, PATCH, DELETE)
│   ├── models.py         ← SQLAlchemy DB table definition
│   ├── schemas.py        ← Pydantic validation models
│   ├── database.py       ← DB connection + session setup
│   ├── requirements.txt  ← Python packages needed
│   └── todos.db          ← SQLite file (auto-created on first run)
└── frontend/
    └── index.html        ← Complete UI (HTML + CSS + JS)
```

## How to Run

### Step 1 — Install packages
```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Start the API server
```bash
uvicorn main:app --reload
```
Server runs at: http://localhost:8000

### Step 3 — Open the frontend
Just open `frontend/index.html` in your browser directly.
(double-click the file or drag it into Chrome)

## API Endpoints

| Method | URL                | What it does              |
|--------|--------------------|---------------------------|
| GET    | /todos             | Get all todos             |
| GET    | /todos?completed=true | Get completed todos    |
| GET    | /todos?priority=high  | Filter by priority     |
| GET    | /todos?search=buy     | Search by title        |
| GET    | /todos/{id}        | Get one todo by ID        |
| POST   | /todos             | Create a new todo         |
| PATCH  | /todos/{id}        | Update a todo partially   |
| DELETE | /todos/{id}        | Delete a todo             |
| GET    | /stats             | Get summary statistics    |
| GET    | /docs              | Swagger UI (auto-docs)    |

## Test with Swagger
Go to http://localhost:8000/docs to test every endpoint live in the browser.
