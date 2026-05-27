from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Used when CREATING a todo (POST) ──────────────────────────
class TodoCreate(BaseModel):
    title:    str  = Field(min_length=1, max_length=200)
    desc:     str  = Field(default="", max_length=500)
    priority: str  = Field(default="medium", pattern="^(low|medium|high)$")


# ── Used when PARTIALLY UPDATING a todo (PATCH) ───────────────
class TodoUpdate(BaseModel):
    title:     Optional[str]  = Field(default=None, min_length=1, max_length=200)
    desc:      Optional[str]  = Field(default=None, max_length=500)
    priority:  Optional[str]  = Field(default=None, pattern="^(low|medium|high)$")
    completed: Optional[bool] = None


# ── Used in RESPONSES — what FastAPI sends back ────────────────
class TodoResponse(BaseModel):
    id:         int
    title:      str
    desc:       str
    priority:   str
    completed:  bool
    created_at: datetime

    class Config:
        from_attributes = True   # allows SQLAlchemy model → Pydantic conversion
