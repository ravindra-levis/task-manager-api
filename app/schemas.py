from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class OrgCreate(BaseModel):
    name: str

class ProjectCreate(BaseModel):
    name: str
    org_id: int

class TaskCreate(BaseModel):
    title: str
    description: str
    project_id: int
    assigned_user_id: int | None = None

class UpdateTask(BaseModel):
    status: TaskStatus

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus

    class Config:
        from_attributes = True


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    project_id: int
    assigned_user_id: Optional[int]

    class Config:
        from_attributes = True

