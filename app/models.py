# models.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Task(BaseModel):
    id: str
    purpose: str
    owner: str
    created_at: datetime
    ttl_days: int
    last_run: Optional[datetime] = None
    run_count: int = 0
    status: str = "active"