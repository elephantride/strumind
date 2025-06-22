from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.element import Element, ElementType
from app.schemas.element import (
    ElementCreate,
    ElementUpdate,
    ElementResponse,
    ElementDetail,
)
from app.crud.element import (
    create_element,
    get_element,
    get_elements,
    get_elements_by_project,
    get_element_detail,
    update_element,
    delete_element,
)

router = APIRouter()


@router.post("/", response_model=ElementResponse, status_code=201)
def create_new_element(
    element_in: ElementCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new element.
    """
    return create_element(db=db, element_in=element_in)


@router.get("/", response_model=List[ElementResponse])
def read_elements(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    element_type: Optional[ElementType] = None,
    material_id: Optional[str] = None,
    section_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve elements.
    """
    if project_id:
        return get_elements_by_project(
            db=db, 
            project_id=project_id, 
            skip=skip, 
            limit=limit, 
            element_type=element_type,
            material_id=material_id,
            section_id=section_id,
        )
    return get_elements(
        db=db, 
        skip=skip, 
        limit=limit, 
        element_type=element_type,
        material_id=material_id,
        section_id=section_id,
    )


@router.get("/{element_id}", response_model=ElementDetail)
def read_element(
    element_id: str,
    db: Session = Depends(get_db),
):
    """
    Get element by ID with detailed information.
    """
    element = get_element_detail(db=db, element_id=element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")
    return element


@router.put("/{element_id}", response_model=ElementResponse)
def update_existing_element(
    element_id: str,
    element_in: ElementUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an element.
    """
    element = get_element(db=db, element_id=element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")
    return update_element(db=db, db_obj=element, obj_in=element_in)


@router.delete("/{element_id}", response_model=ElementResponse)
def delete_existing_element(
    element_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete an element.
    """
    element = get_element(db=db, element_id=element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")
    return delete_element(db=db, db_obj=element)