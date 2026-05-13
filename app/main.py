from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import Base, engine, get_db
from app.dependencies import get_current_user
from app.routes import auth
from app import models, schemas


# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="A FastAPI-based task management system with JWT authentication"
)

# Include authentication routes
app.include_router(auth.router)


# ======================================================
# ROOT ROUTE
# ======================================================

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Task Manager API Running"
    }


# ======================================================
# ORGANIZATION ROUTES
# ======================================================

@app.post("/organizations", tags=["Organizations"])
def create_organization(
    org: schemas.OrgCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Create organization
        organization = models.Organization(
            name=org.name
        )

        db.add(organization)
        db.flush()

        # Add creator as admin
        membership = models.Membership(
            user_id=current_user.id,
            org_id=organization.id,
            role=models.UserRole.admin
        )

        db.add(membership)

        db.commit()
        db.refresh(organization)

        return {
            "message": "Organization created successfully",
            "organization_id": organization.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/organizations/{org_id}", tags=["Organizations"])
def get_organization(
    org_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == org_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    organization = db.query(models.Organization).filter(
        models.Organization.id == org_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    return organization


# ======================================================
# PROJECT ROUTES
# ======================================================

@app.post("/projects", tags=["Projects"])
def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == project.org_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Not part of organization"
        )

    try:
        new_project = models.Project(
            name=project.name,
            org_id=project.org_id
        )

        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        return {
            "message": "Project created successfully",
            "project_id": new_project.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/projects/{project_id}", tags=["Projects"])
def get_project(
    project_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == project.org_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return project


# ======================================================
# TASK ROUTES
# ======================================================

@app.post("/tasks", tags=["Tasks"])
def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == task.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == project.org_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    # Validate assigned user
    if task.assigned_user_id:
        assigned_member = db.query(models.Membership).filter(
            models.Membership.user_id == task.assigned_user_id,
            models.Membership.org_id == project.org_id
        ).first()

        if not assigned_member:
            raise HTTPException(
                status_code=400,
                detail="Assigned user not part of organization"
            )

    try:
        new_task = models.Task(
            title=task.title,
            description=task.description,
            project_id=project.id,
            assigned_user_id=task.assigned_user_id,
            status=models.TaskStatus.TODO
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return {
            "message": "Task created successfully",
            "task_id": new_task.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/tasks", response_model=List[schemas.TaskOut], tags= ["Tasks"])
def get_tasks(
    org_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, le=100),
):
    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == org_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    tasks = db.query(models.Task).join(
        models.Project
    ).filter(
        models.Project.org_id == org_id
    ).offset(skip).limit(limit).all()

    return tasks


@app.patch("/tasks/{task_id}", tags=["Tasks"])
def update_task(
    task_id: int,
    payload: schemas.UpdateTask,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    # Get project
    project = db.query(models.Project).filter(
        models.Project.id == task.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == project.org_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    try:
        task.status = payload.status

        db.commit()
        db.refresh(task)

        return {
            "message": "Task updated successfully",
            "status": task.status
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )