from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.design import Design, DesignCode, DesignMethod
from app.schemas.design import (
    DesignCreate,
    DesignUpdate,
    DesignResponse,
    DesignRunRequest,
    ElementDesignResultResponse,
)
from app.crud.design import (
    create_design,
    get_design,
    get_designs,
    get_designs_by_project,
    update_design,
    delete_design,
    get_element_design_results,
)
from app.core.design.designer import run_design_task

router = APIRouter()


@router.post("/", response_model=DesignResponse, status_code=201)
def create_new_design(
    design_in: DesignCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new design.
    """
    return create_design(db=db, design_in=design_in)


@router.get("/", response_model=List[DesignResponse])
def read_designs(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    design_code: Optional[DesignCode] = None,
    design_method: Optional[DesignMethod] = None,
    is_complete: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve designs.
    """
    if project_id:
        return get_designs_by_project(
            db=db, 
            project_id=project_id, 
            skip=skip, 
            limit=limit, 
            design_code=design_code,
            design_method=design_method,
            is_complete=is_complete,
        )
    return get_designs(
        db=db, 
        skip=skip, 
        limit=limit, 
        design_code=design_code,
        design_method=design_method,
        is_complete=is_complete,
    )


@router.get("/{design_id}", response_model=DesignResponse)
def read_design(
    design_id: str,
    db: Session = Depends(get_db),
):
    """
    Get design by ID.
    """
    design = get_design(db=db, design_id=design_id)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return design


@router.put("/{design_id}", response_model=DesignResponse)
def update_existing_design(
    design_id: str,
    design_in: DesignUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a design.
    """
    design = get_design(db=db, design_id=design_id)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return update_design(db=db, db_obj=design, obj_in=design_in)


@router.delete("/{design_id}", response_model=DesignResponse)
def delete_existing_design(
    design_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a design.
    """
    design = get_design(db=db, design_id=design_id)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return delete_design(db=db, db_obj=design)


@router.post("/run", response_model=DesignResponse)
def run_design(
    run_request: DesignRunRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Run a design.
    """
    design = get_design(db=db, design_id=run_request.design_id)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    
    # Run design in background
    background_tasks.add_task(run_design_task, db, design.id)
    
    return design


@router.get("/{design_id}/element-results", response_model=List[ElementDesignResultResponse])
def read_element_design_results(
    design_id: str,
    element_id: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get element design results for a design.
    """
    design = get_design(db=db, design_id=design_id)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    
    return get_element_design_results(
        db=db,
        design_id=design_id,
        element_id=element_id,
        status=status,
        skip=skip,
        limit=limit,
    )