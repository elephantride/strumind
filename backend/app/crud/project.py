from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.project import Project
from app.models.node import Node
from app.models.element import Element
from app.models.material import Material
from app.models.section import Section
from app.models.load import LoadCase
from app.models.analysis import Analysis
from app.models.design import Design
from app.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_projects(
        self, db: Session, *, skip: int = 0, limit: int = 100, name: Optional[str] = None, is_active: Optional[bool] = None
    ) -> List[Project]:
        """
        Get projects with optional filtering.
        """
        query = db.query(self.model)
        
        if name:
            query = query.filter(self.model.name.ilike(f"%{name}%"))
        
        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def get_project_details(self, db: Session, *, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Get project details including counts of related entities.
        """
        project = db.query(self.model).filter(self.model.id == project_id).first()
        
        if not project:
            return None
        
        # Get counts
        node_count = db.query(func.count(Node.id)).filter(Node.project_id == project_id).scalar() or 0
        element_count = db.query(func.count(Element.id)).filter(Element.project_id == project_id).scalar() or 0
        material_count = db.query(func.count(Material.id)).filter(Material.project_id == project_id).scalar() or 0
        section_count = db.query(func.count(Section.id)).filter(Section.project_id == project_id).scalar() or 0
        load_case_count = db.query(func.count(LoadCase.id)).filter(LoadCase.project_id == project_id).scalar() or 0
        analysis_count = db.query(func.count(Analysis.id)).filter(Analysis.project_id == project_id).scalar() or 0
        design_count = db.query(func.count(Design.id)).filter(Design.project_id == project_id).scalar() or 0
        
        # Create response
        project_data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "client": project.client,
            "is_active": project.is_active,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "node_count": node_count,
            "element_count": element_count,
            "material_count": material_count,
            "section_count": section_count,
            "load_case_count": load_case_count,
            "analysis_count": analysis_count,
            "design_count": design_count,
        }
        
        return project_data


# Create instance for export
project = CRUDProject(Project)


# Convenience functions
def create_project(db: Session, *, project_in: ProjectCreate) -> Project:
    return project.create(db=db, obj_in=project_in)


def get_project(db: Session, *, project_id: str) -> Optional[Project]:
    return project.get(db=db, id=project_id)


def get_projects(
    db: Session, *, skip: int = 0, limit: int = 100, name: Optional[str] = None, is_active: Optional[bool] = None
) -> List[Project]:
    return project.get_projects(db=db, skip=skip, limit=limit, name=name, is_active=is_active)


def update_project(db: Session, *, db_obj: Project, obj_in: ProjectUpdate) -> Project:
    return project.update(db=db, db_obj=db_obj, obj_in=obj_in)


def delete_project(db: Session, *, db_obj: Project) -> Project:
    return project.remove(db=db, id=db_obj.id)


def get_project_details(db: Session, *, project_id: str) -> Optional[Dict[str, Any]]:
    return project.get_project_details(db=db, project_id=project_id)