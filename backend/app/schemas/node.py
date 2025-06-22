from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class NodeBase(BaseModel):
    """
    Base schema for node data.
    """
    name: str = Field(..., description="Node name or identifier")
    x: float = Field(..., description="X coordinate (m)")
    y: float = Field(..., description="Y coordinate (m)")
    z: float = Field(..., description="Z coordinate (m)")
    is_support: bool = Field(False, description="Whether the node is a support")
    
    # Support conditions (if is_support is True)
    restraint_x: Optional[bool] = Field(False, description="Restraint in X direction")
    restraint_y: Optional[bool] = Field(False, description="Restraint in Y direction")
    restraint_z: Optional[bool] = Field(False, description="Restraint in Z direction")
    restraint_rx: Optional[bool] = Field(False, description="Restraint around X axis")
    restraint_ry: Optional[bool] = Field(False, description="Restraint around Y axis")
    restraint_rz: Optional[bool] = Field(False, description="Restraint around Z axis")
    
    # Spring stiffness (if applicable)
    spring_x: Optional[float] = Field(None, description="Spring stiffness in X direction (N/m)")
    spring_y: Optional[float] = Field(None, description="Spring stiffness in Y direction (N/m)")
    spring_z: Optional[float] = Field(None, description="Spring stiffness in Z direction (N/m)")
    spring_rx: Optional[float] = Field(None, description="Spring stiffness around X axis (N·m/rad)")
    spring_ry: Optional[float] = Field(None, description="Spring stiffness around Y axis (N·m/rad)")
    spring_rz: Optional[float] = Field(None, description="Spring stiffness around Z axis (N·m/rad)")


class NodeCreate(NodeBase):
    """
    Schema for creating a new node.
    """
    project_id: str = Field(..., description="Project ID")


class NodeUpdate(BaseModel):
    """
    Schema for updating an existing node.
    """
    name: Optional[str] = Field(None, description="Node name or identifier")
    x: Optional[float] = Field(None, description="X coordinate (m)")
    y: Optional[float] = Field(None, description="Y coordinate (m)")
    z: Optional[float] = Field(None, description="Z coordinate (m)")
    is_support: Optional[bool] = Field(None, description="Whether the node is a support")
    
    # Support conditions
    restraint_x: Optional[bool] = Field(None, description="Restraint in X direction")
    restraint_y: Optional[bool] = Field(None, description="Restraint in Y direction")
    restraint_z: Optional[bool] = Field(None, description="Restraint in Z direction")
    restraint_rx: Optional[bool] = Field(None, description="Restraint around X axis")
    restraint_ry: Optional[bool] = Field(None, description="Restraint around Y axis")
    restraint_rz: Optional[bool] = Field(None, description="Restraint around Z axis")
    
    # Spring stiffness
    spring_x: Optional[float] = Field(None, description="Spring stiffness in X direction (N/m)")
    spring_y: Optional[float] = Field(None, description="Spring stiffness in Y direction (N/m)")
    spring_z: Optional[float] = Field(None, description="Spring stiffness in Z direction (N/m)")
    spring_rx: Optional[float] = Field(None, description="Spring stiffness around X axis (N·m/rad)")
    spring_ry: Optional[float] = Field(None, description="Spring stiffness around Y axis (N·m/rad)")
    spring_rz: Optional[float] = Field(None, description="Spring stiffness around Z axis (N·m/rad)")


class NodeResponse(NodeBase, BaseSchema):
    """
    Schema for node response.
    """
    project_id: str = Field(..., description="Project ID")