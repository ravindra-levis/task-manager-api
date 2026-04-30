from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class OrgCreate(BaseModel):
    name: str
    user_id :int

class ProjectCreate(BaseModel):
    name: str

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_user_id: int 
       
class UpdateTask(BaseModel):
    status: str
        

