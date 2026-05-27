from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List

import models
import schemas
from database import engine, get_db

# Create all tables in the database on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do List API",
    description="A full CRUD API built with FastAPI + SQLite",
    version="1.0.0"
)

# Allow frontend (HTML/React) to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────
#  GET /todos  — fetch all (with filters)
# ─────────────────────────────────────────
@app.get("/todos", response_model=List[schemas.TodoResponse])
def get_todos(
    completed: Optional[bool] = Query(default=None),          # ?completed=true
    priority:  Optional[str]  = Query(default=None),          # ?priority=high
    search:    Optional[str]  = Query(default=None),          # ?search=buy
    db: Session = Depends(get_db)
):
    query = db.query(models.Todo)

    if completed is not None:
        query = query.filter(models.Todo.completed == completed)

    if priority:
        query = query.filter(models.Todo.priority == priority)

    if search:
        query = query.filter(models.Todo.title.contains(search))

    return query.order_by(models.Todo.id.desc()).all()


# ─────────────────────────────────────────
#  GET /todos/{id}  — fetch one by ID
# ─────────────────────────────────────────
@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# ─────────────────────────────────────────
#  POST /todos  — create a new todo
# ─────────────────────────────────────────
@app.post("/todos", response_model=schemas.TodoResponse, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    new_todo = models.Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)   # get the auto-generated id back
    return new_todo


# ─────────────────────────────────────────
#  PATCH /todos/{id}  — partial update
# ─────────────────────────────────────────
@app.patch("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int,
    updates: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Only update fields that were actually sent
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)
    return todo


# ─────────────────────────────────────────
#  DELETE /todos/{id}  — delete a todo
# ─────────────────────────────────────────
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": f"Todo #{todo_id} deleted successfully"}


# ─────────────────────────────────────────
#  GET /stats  — bonus: summary stats
# ─────────────────────────────────────────
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total     = db.query(models.Todo).count()
    done      = db.query(models.Todo).filter(models.Todo.completed == True).count()
    pending   = total - done
    high      = db.query(models.Todo).filter(models.Todo.priority == "high").count()
    return {
        "total": total,
        "completed": done,
        "pending": pending,
        "high_priority": high
    }
