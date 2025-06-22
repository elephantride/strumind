from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetail,
)
from app.crud.project import (
    create_project,
    get_project,
    get_projects,
    update_project,
    delete_project,
    get_project_details,
)

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_new_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new project.
    """
    return create_project(db=db, project_in=project_in)


@router.get("/", response_model=List[ProjectResponse])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve projects.
    """
    return get_projects(
        db=db, skip=skip, limit=limit, name=name, is_active=is_active
    )


@router.get("/{project_id}", response_model=ProjectDetail)
def read_project(
    project_id: str,
    db: Session = Depends(get_db),
):
    """
    Get project by ID.
    """
    project = get_project_details(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_existing_project(
    project_id: str,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a project.
    """
    project = get_project(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return update_project(db=db, db_obj=project, obj_in=project_in)


@router.delete("/{project_id}", response_model=ProjectResponse)
def delete_existing_project(
    project_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a project.
    """
    project = get_project(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return delete_project(db=db, db_obj=project)