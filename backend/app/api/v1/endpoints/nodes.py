from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.node import Node
from app.schemas.node import (
    NodeCreate,
    NodeUpdate,
    NodeResponse,
)
from app.crud.node import (
    create_node,
    get_node,
    get_nodes,
    get_nodes_by_project,
    update_node,
    delete_node,
)

router = APIRouter()


@router.post("/", response_model=NodeResponse, status_code=201)
def create_new_node(
    node_in: NodeCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new node.
    """
    return create_node(db=db, node_in=node_in)


@router.get("/", response_model=List[NodeResponse])
def read_nodes(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    is_support: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve nodes.
    """
    if project_id:
        return get_nodes_by_project(
            db=db, project_id=project_id, skip=skip, limit=limit, is_support=is_support
        )
    return get_nodes(
        db=db, skip=skip, limit=limit, is_support=is_support
    )


@router.get("/{node_id}", response_model=NodeResponse)
def read_node(
    node_id: str,
    db: Session = Depends(get_db),
):
    """
    Get node by ID.
    """
    node = get_node(db=db, node_id=node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.put("/{node_id}", response_model=NodeResponse)
def update_existing_node(
    node_id: str,
    node_in: NodeUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a node.
    """
    node = get_node(db=db, node_id=node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return update_node(db=db, db_obj=node, obj_in=node_in)


@router.delete("/{node_id}", response_model=NodeResponse)
def delete_existing_node(
    node_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a node.
    """
    node = get_node(db=db, node_id=node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return delete_node(db=db, db_obj=node)