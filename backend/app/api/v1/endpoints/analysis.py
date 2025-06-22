from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.analysis import Analysis, AnalysisType
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisUpdate,
    AnalysisResponse,
    AnalysisRunRequest,
    NodeResultResponse,
    ElementResultResponse,
    ModalResultResponse,
)
from app.crud.analysis import (
    create_analysis,
    get_analysis,
    get_analyses,
    get_analyses_by_project,
    update_analysis,
    delete_analysis,
    get_node_results,
    get_element_results,
    get_modal_results,
)
from app.core.analysis.solver import run_analysis_task

router = APIRouter()


@router.post("/", response_model=AnalysisResponse, status_code=201)
def create_new_analysis(
    analysis_in: AnalysisCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new analysis.
    """
    return create_analysis(db=db, analysis_in=analysis_in)


@router.get("/", response_model=List[AnalysisResponse])
def read_analyses(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    analysis_type: Optional[AnalysisType] = None,
    is_complete: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve analyses.
    """
    if project_id:
        return get_analyses_by_project(
            db=db, 
            project_id=project_id, 
            skip=skip, 
            limit=limit, 
            analysis_type=analysis_type,
            is_complete=is_complete,
        )
    return get_analyses(
        db=db, 
        skip=skip, 
        limit=limit, 
        analysis_type=analysis_type,
        is_complete=is_complete,
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def read_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    """
    Get analysis by ID.
    """
    analysis = get_analysis(db=db, analysis_id=analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@router.put("/{analysis_id}", response_model=AnalysisResponse)
def update_existing_analysis(
    analysis_id: str,
    analysis_in: AnalysisUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an analysis.
    """
    analysis = get_analysis(db=db, analysis_id=analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return update_analysis(db=db, db_obj=analysis, obj_in=analysis_in)


@router.delete("/{analysis_id}", response_model=AnalysisResponse)
def delete_existing_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete an analysis.
    """
    analysis = get_analysis(db=db, analysis_id=analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return delete_analysis(db=db, db_obj=analysis)


@router.post("/run", response_model=AnalysisResponse)
def run_analysis(
    run_request: AnalysisRunRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Run an analysis.
    """
    analysis = get_analysis(db=db, analysis_id=run_request.analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Run analysis in background
    background_tasks.add_task(run_analysis_task, db, analysis.id)
    
    return analysis


@router.get("/{analysis_id}/node-results", response_model=List[NodeResultResponse])
def read_node_results(
    analysis_id: str,
    node_id: Optional[str] = None,
    load_case_id: Optional[str] = None,
    load_combination_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get node results for an analysis.
    """
    analysis = get_analysis(db=db, analysis_id=analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return get_node_results(
        db=db,
        analysis_id=analysis_id,
        node_id=node_id,
        load_case_id=load_case_id,
        load_combination_id=load_combination_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{analysis_id}/element-results", response_model=List[ElementResultResponse])
def read_element_results(
    analysis_id: str,
    element_id: Optional[str] = None,
    load_case_id: Optional[str] = None,
    load_combination_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get element results for an analysis.
    """
    analysis = get_analysis(db=db, analysis_id=analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return get_element_results(
        db=db,
        analysis_id=analysis_id,
        element_id=element_id,
        load_case_id=load_case_id,
        load_combination_id=load_combination_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{analysis_id}/modal-results", response_model=List[ModalResultResponse])
def read_modal_results(
    analysis_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get modal results for an analysis.
    """
    analysis = get_analysis(db=db, analysis_id=analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analysis.analysis_type not in [AnalysisType.MODAL, AnalysisType.RESPONSE_SPECTRUM]:
        raise HTTPException(status_code=400, detail="Analysis is not a modal or response spectrum analysis")
    
    return get_modal_results(
        db=db,
        analysis_id=analysis_id,
        skip=skip,
        limit=limit,
    )