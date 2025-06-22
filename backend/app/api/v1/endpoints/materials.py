from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.material import Material, MaterialType
from app.schemas.material import (
    MaterialCreate,
    MaterialUpdate,
    MaterialResponse,
)
from app.crud.material import (
    create_material,
    get_material,
    get_materials,
    get_materials_by_project,
    update_material,
    delete_material,
)

router = APIRouter()


@router.post("/", response_model=MaterialResponse, status_code=201)
def create_new_material(
    material_in: MaterialCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new material.
    """
    return create_material(db=db, material_in=material_in)


@router.get("/", response_model=List[MaterialResponse])
def read_materials(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    material_type: Optional[MaterialType] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve materials.
    """
    if project_id:
        return get_materials_by_project(
            db=db, project_id=project_id, skip=skip, limit=limit, material_type=material_type
        )
    return get_materials(
        db=db, skip=skip, limit=limit, material_type=material_type
    )


@router.get("/{material_id}", response_model=MaterialResponse)
def read_material(
    material_id: str,
    db: Session = Depends(get_db),
):
    """
    Get material by ID.
    """
    material = get_material(db=db, material_id=material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@router.put("/{material_id}", response_model=MaterialResponse)
def update_existing_material(
    material_id: str,
    material_in: MaterialUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a material.
    """
    material = get_material(db=db, material_id=material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return update_material(db=db, db_obj=material, obj_in=material_in)


@router.delete("/{material_id}", response_model=MaterialResponse)
def delete_existing_material(
    material_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a material.
    """
    material = get_material(db=db, material_id=material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return delete_material(db=db, db_obj=material)