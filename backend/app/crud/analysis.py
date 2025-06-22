from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.analysis import Analysis, AnalysisType, NodeResult, ElementResult, ModalResult
from app.schemas.analysis import AnalysisCreate, AnalysisUpdate


class CRUDAnalysis(CRUDBase[Analysis, AnalysisCreate, AnalysisUpdate]):
    def get_analyses(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100, 
        analysis_type: Optional[AnalysisType] = None,
        is_complete: Optional[bool] = None,
    ) -> List[Analysis]:
        """
        Get analyses with optional filtering.
        """
        query = db.query(self.model)
        
        if analysis_type:
            query = query.filter(self.model.analysis_type == analysis_type)
        
        if is_complete is not None:
            query = query.filter(self.model.is_complete == is_complete)
        
        return query.offset(skip).limit(limit).all()
    
    def get_analyses_by_project(
        self, 
        db: Session, 
        *, 
        project_id: str, 
        skip: int = 0, 
        limit: int = 100, 
        analysis_type: Optional[AnalysisType] = None,
        is_complete: Optional[bool] = None,
    ) -> List[Analysis]:
        """
        Get analyses by project ID with optional filtering.
        """
        query = db.query(self.model).filter(self.model.project_id == project_id)
        
        if analysis_type:
            query = query.filter(self.model.analysis_type == analysis_type)
        
        if is_complete is not None:
            query = query.filter(self.model.is_complete == is_complete)
        
        return query.offset(skip).limit(limit).all()
    
    def get_node_results(
        self,
        db: Session,
        *,
        analysis_id: str,
        node_id: Optional[str] = None,
        load_case_id: Optional[str] = None,
        load_combination_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[NodeResult]:
        """
        Get node results for an analysis.
        """
        query = db.query(NodeResult).filter(NodeResult.analysis_id == analysis_id)
        
        if node_id:
            query = query.filter(NodeResult.node_id == node_id)
        
        if load_case_id:
            query = query.filter(NodeResult.load_case_id == load_case_id)
        
        if load_combination_id:
            query = query.filter(NodeResult.load_combination_id == load_combination_id)
        
        return query.offset(skip).limit(limit).all()
    
    def get_element_results(
        self,
        db: Session,
        *,
        analysis_id: str,
        element_id: Optional[str] = None,
        load_case_id: Optional[str] = None,
        load_combination_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ElementResult]:
        """
        Get element results for an analysis.
        """
        query = db.query(ElementResult).filter(ElementResult.analysis_id == analysis_id)
        
        if element_id:
            query = query.filter(ElementResult.element_id == element_id)
        
        if load_case_id:
            query = query.filter(ElementResult.load_case_id == load_case_id)
        
        if load_combination_id:
            query = query.filter(ElementResult.load_combination_id == load_combination_id)
        
        return query.offset(skip).limit(limit).all()
    
    def get_modal_results(
        self,
        db: Session,
        *,
        analysis_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModalResult]:
        """
        Get modal results for an analysis.
        """
        query = db.query(ModalResult).filter(ModalResult.analysis_id == analysis_id)
        
        return query.order_by(ModalResult.mode_number).offset(skip).limit(limit).all()


# Create instance for export
analysis = CRUDAnalysis(Analysis)


# Convenience functions
def create_analysis(db: Session, *, analysis_in: AnalysisCreate) -> Analysis:
    return analysis.create(db=db, obj_in=analysis_in)


def get_analysis(db: Session, *, analysis_id: str) -> Optional[Analysis]:
    return analysis.get(db=db, id=analysis_id)


def get_analyses(
    db: Session, 
    *, 
    skip: int = 0, 
    limit: int = 100, 
    analysis_type: Optional[AnalysisType] = None,
    is_complete: Optional[bool] = None,
) -> List[Analysis]:
    return analysis.get_analyses(
        db=db, 
        skip=skip, 
        limit=limit, 
        analysis_type=analysis_type,
        is_complete=is_complete,
    )


def get_analyses_by_project(
    db: Session, 
    *, 
    project_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    analysis_type: Optional[AnalysisType] = None,
    is_complete: Optional[bool] = None,
) -> List[Analysis]:
    return analysis.get_analyses_by_project(
        db=db, 
        project_id=project_id, 
        skip=skip, 
        limit=limit, 
        analysis_type=analysis_type,
        is_complete=is_complete,
    )


def update_analysis(db: Session, *, db_obj: Analysis, obj_in: AnalysisUpdate) -> Analysis:
    return analysis.update(db=db, db_obj=db_obj, obj_in=obj_in)


def delete_analysis(db: Session, *, db_obj: Analysis) -> Analysis:
    return analysis.remove(db=db, id=db_obj.id)


def get_node_results(
    db: Session,
    *,
    analysis_id: str,
    node_id: Optional[str] = None,
    load_case_id: Optional[str] = None,
    load_combination_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[NodeResult]:
    return analysis.get_node_results(
        db=db,
        analysis_id=analysis_id,
        node_id=node_id,
        load_case_id=load_case_id,
        load_combination_id=load_combination_id,
        skip=skip,
        limit=limit,
    )


def get_element_results(
    db: Session,
    *,
    analysis_id: str,
    element_id: Optional[str] = None,
    load_case_id: Optional[str] = None,
    load_combination_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[ElementResult]:
    return analysis.get_element_results(
        db=db,
        analysis_id=analysis_id,
        element_id=element_id,
        load_case_id=load_case_id,
        load_combination_id=load_combination_id,
        skip=skip,
        limit=limit,
    )


def get_modal_results(
    db: Session,
    *,
    analysis_id: str,
    skip: int = 0,
    limit: int = 100,
) -> List[ModalResult]:
    return analysis.get_modal_results(
        db=db,
        analysis_id=analysis_id,
        skip=skip,
        limit=limit,
    )