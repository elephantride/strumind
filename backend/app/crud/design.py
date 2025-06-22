from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.design import Design, DesignCode, DesignMethod, ElementDesignResult
from app.schemas.design import DesignCreate, DesignUpdate


class CRUDDesign(CRUDBase[Design, DesignCreate, DesignUpdate]):
    def get_designs(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100, 
        design_code: Optional[DesignCode] = None,
        design_method: Optional[DesignMethod] = None,
        is_complete: Optional[bool] = None,
    ) -> List[Design]:
        """
        Get designs with optional filtering.
        """
        query = db.query(self.model)
        
        if design_code:
            query = query.filter(self.model.design_code == design_code)
        
        if design_method:
            query = query.filter(self.model.design_method == design_method)
        
        if is_complete is not None:
            query = query.filter(self.model.is_complete == is_complete)
        
        return query.offset(skip).limit(limit).all()
    
    def get_designs_by_project(
        self, 
        db: Session, 
        *, 
        project_id: str, 
        skip: int = 0, 
        limit: int = 100, 
        design_code: Optional[DesignCode] = None,
        design_method: Optional[DesignMethod] = None,
        is_complete: Optional[bool] = None,
    ) -> List[Design]:
        """
        Get designs by project ID with optional filtering.
        """
        query = db.query(self.model).filter(self.model.project_id == project_id)
        
        if design_code:
            query = query.filter(self.model.design_code == design_code)
        
        if design_method:
            query = query.filter(self.model.design_method == design_method)
        
        if is_complete is not None:
            query = query.filter(self.model.is_complete == is_complete)
        
        return query.offset(skip).limit(limit).all()
    
    def get_element_design_results(
        self,
        db: Session,
        *,
        design_id: str,
        element_id: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ElementDesignResult]:
        """
        Get element design results for a design.
        """
        query = db.query(ElementDesignResult).filter(ElementDesignResult.design_id == design_id)
        
        if element_id:
            query = query.filter(ElementDesignResult.element_id == element_id)
        
        if status:
            query = query.filter(ElementDesignResult.status == status)
        
        return query.offset(skip).limit(limit).all()


# Create instance for export
design = CRUDDesign(Design)


# Convenience functions
def create_design(db: Session, *, design_in: DesignCreate) -> Design:
    return design.create(db=db, obj_in=design_in)


def get_design(db: Session, *, design_id: str) -> Optional[Design]:
    return design.get(db=db, id=design_id)


def get_designs(
    db: Session, 
    *, 
    skip: int = 0, 
    limit: int = 100, 
    design_code: Optional[DesignCode] = None,
    design_method: Optional[DesignMethod] = None,
    is_complete: Optional[bool] = None,
) -> List[Design]:
    return design.get_designs(
        db=db, 
        skip=skip, 
        limit=limit, 
        design_code=design_code,
        design_method=design_method,
        is_complete=is_complete,
    )


def get_designs_by_project(
    db: Session, 
    *, 
    project_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    design_code: Optional[DesignCode] = None,
    design_method: Optional[DesignMethod] = None,
    is_complete: Optional[bool] = None,
) -> List[Design]:
    return design.get_designs_by_project(
        db=db, 
        project_id=project_id, 
        skip=skip, 
        limit=limit, 
        design_code=design_code,
        design_method=design_method,
        is_complete=is_complete,
    )


def update_design(db: Session, *, db_obj: Design, obj_in: DesignUpdate) -> Design:
    return design.update(db=db, db_obj=db_obj, obj_in=obj_in)


def delete_design(db: Session, *, db_obj: Design) -> Design:
    return design.remove(db=db, id=db_obj.id)


def get_element_design_results(
    db: Session,
    *,
    design_id: str,
    element_id: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[ElementDesignResult]:
    return design.get_element_design_results(
        db=db,
        design_id=design_id,
        element_id=element_id,
        status=status,
        skip=skip,
        limit=limit,
    )