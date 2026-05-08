from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship 
from .database import Base
import enum

class TaskStatus(str, enum.Enum):
    todo = "TODO"
    in_progress = "IN_PROGRESS"
    done = "DONE"
    
class UserRole(str, enum.Enum):
    admin = "ADMIN"
    member = "MEMBER"
    viewer = "VIEWER"
    
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    projects = relationship("Project", back_populates="organization")
    memberships = relationship("Membership", back_populates="organization")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    memberships = relationship("Membership", back_populates="user")
    tasks = relationship("Task", back_populates="assigned_user")
    
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    org_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

    status = Column(Enum(TaskStatus), default=TaskStatus.todo)

    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_user_id = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project", back_populates="tasks")
    assigned_user = relationship("User", back_populates="tasks")
    
class Membership(Base):
    __tablename__ = "memberships"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), primary_key=True)
    role = Column(Enum(UserRole), nullable=False)

    user = relationship("User", back_populates="memberships")
    organization = relationship("Organization", back_populates="memberships")