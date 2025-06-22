from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import math

from app.crud.base import CRUDBase
from app.models.element import Element, ElementType
from app.schemas.element import ElementCreate, ElementUpdate


class CRUDElement(CRUDBase[Element, ElementCreate, ElementUpdate]):
    def get_elements(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100, 
        element_type: Optional[ElementType] = None,
        material_id: Optional[str] = None,
        section_id: Optional[str] = None,
    ) -> List[Element]:
        """
        Get elements with optional filtering.
        """
        query = db.query(self.model)
        
        if element_type:
            query = query.filter(self.model.element_type == element_type)
        
        if material_id:
            query = query.filter(self.model.material_id == material_id)
        
        if section_id:
            query = query.filter(self.model.section_id == section_id)
        
        return query.offset(skip).limit(limit).all()
    
    def get_elements_by_project(
        self, 
        db: Session, 
        *, 
        project_id: str, 
        skip: int = 0, 
        limit: int = 100, 
        element_type: Optional[ElementType] = None,
        material_id: Optional[str] = None,
        section_id: Optional[str] = None,
    ) -> List[Element]:
        """
        Get elements by project ID with optional filtering.
        """
        query = db.query(self.model).filter(self.model.project_id == project_id)
        
        if element_type:
            query = query.filter(self.model.element_type == element_type)
        
        if material_id:
            query = query.filter(self.model.material_id == material_id)
        
        if section_id:
            query = query.filter(self.model.section_id == section_id)
        
        return query.offset(skip).limit(limit).all()
    
    def get_element_detail(self, db: Session, *, element_id: str) -> Optional[Dict[str, Any]]:
        """
        Get element details including related entities.
        """
        element = db.query(self.model).filter(self.model.id == element_id).first()
        
        if not element:
            return None
        
        # Calculate length
        start_node = element.start_node
        end_node = element.end_node
        
        dx = end_node.x - start_node.x
        dy = end_node.y - start_node.y
        dz = end_node.z - start_node.z
        
        length = math.sqrt(dx**2 + dy**2 + dz**2)
        
        # Create response
        element_data = {
            "id": element.id,
            "project_id": element.project_id,
            "name": element.name,
            "element_type": element.element_type,
            "start_node_id": element.start_node_id,
            "end_node_id": element.end_node_id,
            "section_id": element.section_id,
            "material_id": element.material_id,
            "angle": element.angle,
            "release_start_x": element.release_start_x,
            "release_start_y": element.release_start_y,
            "release_start_z": element.release_start_z,
            "release_start_rx": element.release_start_rx,
            "release_start_ry": element.release_start_ry,
            "release_start_rz": element.release_start_rz,
            "release_end_x": element.release_end_x,
            "release_end_y": element.release_end_y,
            "release_end_z": element.release_end_z,
            "release_end_rx": element.release_end_rx,
            "release_end_ry": element.release_end_ry,
            "release_end_rz": element.release_end_rz,
            "created_at": element.created_at,
            "updated_at": element.updated_at,
            "length": length,
            "start_node": {
                "id": start_node.id,
                "name": start_node.name,
                "x": start_node.x,
                "y": start_node.y,
                "z": start_node.z,
                "is_support": start_node.is_support,
            },
            "end_node": {
                "id": end_node.id,
                "name": end_node.name,
                "x": end_node.x,
                "y": end_node.y,
                "z": end_node.z,
                "is_support": end_node.is_support,
            },
            "section": {
                "id": element.section.id,
                "name": element.section.name,
                "section_type": element.section.section_type,
                "area": element.section.area,
            },
            "material": {
                "id": element.material.id,
                "name": element.material.name,
                "material_type": element.material.material_type,
                "elastic_modulus": element.material.elastic_modulus,
            },
        }
        
        return element_data


# Create instance for export
element = CRUDElement(Element)


# Convenience functions
def create_element(db: Session, *, element_in: ElementCreate) -> Element:
    return element.create(db=db, obj_in=element_in)


def get_element(db: Session, *, element_id: str) -> Optional[Element]:
    return element.get(db=db, id=element_id)


def get_elements(
    db: Session, 
    *, 
    skip: int = 0, 
    limit: int = 100, 
    element_type: Optional[ElementType] = None,
    material_id: Optional[str] = None,
    section_id: Optional[str] = None,
) -> List[Element]:
    return element.get_elements(
        db=db, 
        skip=skip, 
        limit=limit, 
        element_type=element_type,
        material_id=material_id,
        section_id=section_id,
    )


def get_elements_by_project(
    db: Session, 
    *, 
    project_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    element_type: Optional[ElementType] = None,
    material_id: Optional[str] = None,
    section_id: Optional[str] = None,
) -> List[Element]:
    return element.get_elements_by_project(
        db=db, 
        project_id=project_id, 
        skip=skip, 
        limit=limit, 
        element_type=element_type,
        material_id=material_id,
        section_id=section_id,
    )


def get_element_detail(db: Session, *, element_id: str) -> Optional[Dict[str, Any]]:
    return element.get_element_detail(db=db, element_id=element_id)


def update_element(db: Session, *, db_obj: Element, obj_in: ElementUpdate) -> Element:
    return element.update(db=db, db_obj=db_obj, obj_in=obj_in)


def delete_element(db: Session, *, db_obj: Element) -> Element:
    return element.remove(db=db, id=db_obj.id)