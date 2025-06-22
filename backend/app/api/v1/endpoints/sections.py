from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.section import Section, SectionType
from app.schemas.section import (
    SectionCreate,
    SectionUpdate,
    SectionResponse,
)
from app.crud.section import (
    create_section,
    get_section,
    get_sections,
    get_sections_by_project,
    update_section,
    delete_section,
)

router = APIRouter()


@router.post("/", response_model=SectionResponse, status_code=201)
def create_new_section(
    section_in: SectionCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new section.
    """
    return create_section(db=db, section_in=section_in)


@router.get("/", response_model=List[SectionResponse])
def read_sections(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    section_type: Optional[SectionType] = None,
    material_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve sections.
    """
    if project_id:
        return get_sections_by_project(
            db=db, 
            project_id=project_id, 
            skip=skip, 
            limit=limit, 
            section_type=section_type,
            material_id=material_id,
        )
    return get_sections(
        db=db, 
        skip=skip, 
        limit=limit, 
        section_type=section_type,
        material_id=material_id,
    )


@router.get("/{section_id}", response_model=SectionResponse)
def read_section(
    section_id: str,
    db: Session = Depends(get_db),
):
    """
    Get section by ID.
    """
    section = get_section(db=db, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.put("/{section_id}", response_model=SectionResponse)
def update_existing_section(
    section_id: str,
    section_in: SectionUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a section.
    """
    section = get_section(db=db, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return update_section(db=db, db_obj=section, obj_in=section_in)


@router.delete("/{section_id}", response_model=SectionResponse)
def delete_existing_section(
    section_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a section.
    """
    section = get_section(db=db, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return delete_section(db=db, db_obj=section)