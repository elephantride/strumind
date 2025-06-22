from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.load import Load, LoadType, LoadCase, LoadCombination
from app.schemas.load import (
    LoadCreate,
    LoadUpdate,
    LoadResponse,
    LoadCaseCreate,
    LoadCaseUpdate,
    LoadCaseResponse,
    LoadCombinationCreate,
    LoadCombinationUpdate,
    LoadCombinationResponse,
)
from app.crud.load import (
    create_load,
    get_load,
    get_loads,
    get_loads_by_project,
    update_load,
    delete_load,
    create_load_case,
    get_load_case,
    get_load_cases,
    get_load_cases_by_project,
    update_load_case,
    delete_load_case,
    create_load_combination,
    get_load_combination,
    get_load_combinations,
    get_load_combinations_by_project,
    update_load_combination,
    delete_load_combination,
)

router = APIRouter()


# Load Case endpoints
@router.post("/cases", response_model=LoadCaseResponse, status_code=201)
def create_new_load_case(
    load_case_in: LoadCaseCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new load case.
    """
    return create_load_case(db=db, load_case_in=load_case_in)


@router.get("/cases", response_model=List[LoadCaseResponse])
def read_load_cases(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve load cases.
    """
    if project_id:
        return get_load_cases_by_project(
            db=db, project_id=project_id, skip=skip, limit=limit, is_active=is_active
        )
    return get_load_cases(
        db=db, skip=skip, limit=limit, is_active=is_active
    )


@router.get("/cases/{load_case_id}", response_model=LoadCaseResponse)
def read_load_case(
    load_case_id: str,
    db: Session = Depends(get_db),
):
    """
    Get load case by ID.
    """
    load_case = get_load_case(db=db, load_case_id=load_case_id)
    if not load_case:
        raise HTTPException(status_code=404, detail="Load case not found")
    return load_case


@router.put("/cases/{load_case_id}", response_model=LoadCaseResponse)
def update_existing_load_case(
    load_case_id: str,
    load_case_in: LoadCaseUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a load case.
    """
    load_case = get_load_case(db=db, load_case_id=load_case_id)
    if not load_case:
        raise HTTPException(status_code=404, detail="Load case not found")
    return update_load_case(db=db, db_obj=load_case, obj_in=load_case_in)


@router.delete("/cases/{load_case_id}", response_model=LoadCaseResponse)
def delete_existing_load_case(
    load_case_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a load case.
    """
    load_case = get_load_case(db=db, load_case_id=load_case_id)
    if not load_case:
        raise HTTPException(status_code=404, detail="Load case not found")
    return delete_load_case(db=db, db_obj=load_case)


# Load Combination endpoints
@router.post("/combinations", response_model=LoadCombinationResponse, status_code=201)
def create_new_load_combination(
    load_combination_in: LoadCombinationCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new load combination.
    """
    return create_load_combination(db=db, load_combination_in=load_combination_in)


@router.get("/combinations", response_model=List[LoadCombinationResponse])
def read_load_combinations(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve load combinations.
    """
    if project_id:
        return get_load_combinations_by_project(
            db=db, project_id=project_id, skip=skip, limit=limit, is_active=is_active
        )
    return get_load_combinations(
        db=db, skip=skip, limit=limit, is_active=is_active
    )


@router.get("/combinations/{load_combination_id}", response_model=LoadCombinationResponse)
def read_load_combination(
    load_combination_id: str,
    db: Session = Depends(get_db),
):
    """
    Get load combination by ID.
    """
    load_combination = get_load_combination(db=db, load_combination_id=load_combination_id)
    if not load_combination:
        raise HTTPException(status_code=404, detail="Load combination not found")
    return load_combination


@router.put("/combinations/{load_combination_id}", response_model=LoadCombinationResponse)
def update_existing_load_combination(
    load_combination_id: str,
    load_combination_in: LoadCombinationUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a load combination.
    """
    load_combination = get_load_combination(db=db, load_combination_id=load_combination_id)
    if not load_combination:
        raise HTTPException(status_code=404, detail="Load combination not found")
    return update_load_combination(db=db, db_obj=load_combination, obj_in=load_combination_in)


@router.delete("/combinations/{load_combination_id}", response_model=LoadCombinationResponse)
def delete_existing_load_combination(
    load_combination_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a load combination.
    """
    load_combination = get_load_combination(db=db, load_combination_id=load_combination_id)
    if not load_combination:
        raise HTTPException(status_code=404, detail="Load combination not found")
    return delete_load_combination(db=db, db_obj=load_combination)


# Load endpoints
@router.post("/", response_model=LoadResponse, status_code=201)
def create_new_load(
    load_in: LoadCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new load.
    """
    return create_load(db=db, load_in=load_in)


@router.get("/", response_model=List[LoadResponse])
def read_loads(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    load_case_id: Optional[str] = None,
    load_type: Optional[LoadType] = None,
    node_id: Optional[str] = None,
    element_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve loads.
    """
    if project_id:
        return get_loads_by_project(
            db=db, 
            project_id=project_id, 
            skip=skip, 
            limit=limit, 
            load_case_id=load_case_id,
            load_type=load_type,
            node_id=node_id,
            element_id=element_id,
        )
    return get_loads(
        db=db, 
        skip=skip, 
        limit=limit, 
        load_case_id=load_case_id,
        load_type=load_type,
        node_id=node_id,
        element_id=element_id,
    )


@router.get("/{load_id}", response_model=LoadResponse)
def read_load(
    load_id: str,
    db: Session = Depends(get_db),
):
    """
    Get load by ID.
    """
    load = get_load(db=db, load_id=load_id)
    if not load:
        raise HTTPException(status_code=404, detail="Load not found")
    return load


@router.put("/{load_id}", response_model=LoadResponse)
def update_existing_load(
    load_id: str,
    load_in: LoadUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a load.
    """
    load = get_load(db=db, load_id=load_id)
    if not load:
        raise HTTPException(status_code=404, detail="Load not found")
    return update_load(db=db, db_obj=load, obj_in=load_in)


@router.delete("/{load_id}", response_model=LoadResponse)
def delete_existing_load(
    load_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a load.
    """
    load = get_load(db=db, load_id=load_id)
    if not load:
        raise HTTPException(status_code=404, detail="Load not found")
    return delete_load(db=db, db_obj=load)