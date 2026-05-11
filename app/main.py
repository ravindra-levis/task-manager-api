from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.routes import auth
from app.database import get_db, Base, engine
from app.dependencies import get_current_user
from app import schemas
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "TaskFlow API Running"}


# =================== ORGANIZATION =================

@app.post("/organizations")
def create_organization(
    org: schemas.OrgCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    organization = models.Organization(name=org.name)

    db.add(organization)
    db.commit()
    db.refresh(organization)

    membership = models.Membership(
        user_id=current_user.id,
        org_id=organization.id,
        role=models.UserRole.admin
    )

    db.add(membership)
    db.commit()

    return {
        "message": "Organization created",
        "organization_id": organization.id
    }


@app.get("/organizations/{org_id}")
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
        raise HTTPException(status_code=403, detail="Access denied")

    organization = db.query(models.Organization).filter(
        models.Organization.id == org_id
    ).first()

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return organization


# =================== PROJECT ======================

@app.post("/projects")
def create_project(
    prj: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == prj.org_id
    ).first()

    if not membership:
        raise HTTPException(status_code=403, detail="Not part of organization")

    project = models.Project(
        name=prj.name,
        org_id=prj.org_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "message": "Project created",
        "project_id": project.id
    }


@app.get("/projects/{project_id}")
def get_project(
    project_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == project.org_id
    ).first()

    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")

    return project


# ======================= TASK =====================

@app.post("/tasks")
def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == task.project_id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == project.org_id
    ).first()

    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")

    if task.assigned_user_id:
        assigned_member = db.query(models.Membership).filter(
            models.Membership.user_id == task.assigned_user_id,
            models.Membership.org_id == project.org_id
        ).first()

        if not assigned_member:
            raise HTTPException(
                status_code=400,
                detail="Assigned user not in organization"
            )

    task = models.Task(
        title=task.title,
        description=task.description,
        project_id=project.id,
        org_id=project.org_id,
        assigned_user_id=task.assigned_user_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "message": "Task created",
        "task_id": task.id
    }

@app.get("/tasks")
def get_tasks(
    org_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
):
    membership = db.query(models.Membership).filter(
        models.Membership.user_id == current_user.id,
        models.Membership.org_id == org_id
    ).first()

    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")

    tasks = db.query(models.Task).filter(
        models.Task.org_id == org_id
    ).offset(skip).limit(limit).all()  

    return tasks