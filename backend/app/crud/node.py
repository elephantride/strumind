from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.node import Node
from app.schemas.node import NodeCreate, NodeUpdate


class CRUDNode(CRUDBase[Node, NodeCreate, NodeUpdate]):
    def get_nodes(
        self, db: Session, *, skip: int = 0, limit: int = 100, is_support: Optional[bool] = None
    ) -> List[Node]:
        """
        Get nodes with optional filtering.
        """
        query = db.query(self.model)
        
        if is_support is not None:
            query = query.filter(self.model.is_support == is_support)
        
        return query.offset(skip).limit(limit).all()
    
    def get_nodes_by_project(
        self, db: Session, *, project_id: str, skip: int = 0, limit: int = 100, is_support: Optional[bool] = None
    ) -> List[Node]:
        """
        Get nodes by project ID with optional filtering.
        """
        query = db.query(self.model).filter(self.model.project_id == project_id)
        
        if is_support is not None:
            query = query.filter(self.model.is_support == is_support)
        
        return query.offset(skip).limit(limit).all()


# Create instance for export
node = CRUDNode(Node)


# Convenience functions
def create_node(db: Session, *, node_in: NodeCreate) -> Node:
    return node.create(db=db, obj_in=node_in)


def get_node(db: Session, *, node_id: str) -> Optional[Node]:
    return node.get(db=db, id=node_id)


def get_nodes(
    db: Session, *, skip: int = 0, limit: int = 100, is_support: Optional[bool] = None
) -> List[Node]:
    return node.get_nodes(db=db, skip=skip, limit=limit, is_support=is_support)


def get_nodes_by_project(
    db: Session, *, project_id: str, skip: int = 0, limit: int = 100, is_support: Optional[bool] = None
) -> List[Node]:
    return node.get_nodes_by_project(
        db=db, project_id=project_id, skip=skip, limit=limit, is_support=is_support
    )


def update_node(db: Session, *, db_obj: Node, obj_in: NodeUpdate) -> Node:
    return node.update(db=db, db_obj=db_obj, obj_in=obj_in)


def delete_node(db: Session, *, db_obj: Node) -> Node:
    return node.remove(db=db, id=db_obj.id)