from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.models.element import ElementType
from app.schemas.base import BaseSchema


class ElementBase(BaseModel):
    """
    Base schema for element data.
    """
    name: str = Field(..., description="Element name or identifier")
    element_type: ElementType = Field(..., description="Element type")
    start_node_id: str = Field(..., description="Start node ID")
    end_node_id: str = Field(..., description="End node ID")
    section_id: str = Field(..., description="Section ID")
    material_id: str = Field(..., description="Material ID")
    angle: float = Field(0.0, description="Rotation angle in degrees")
    
    # Release conditions
    release_start_x: bool = Field(False, description="Release translation X at start")
    release_start_y: bool = Field(False, description="Release translation Y at start")
    release_start_z: bool = Field(False, description="Release translation Z at start")
    release_start_rx: bool = Field(False, description="Release rotation X at start")
    release_start_ry: bool = Field(False, description="Release rotation Y at start")
    release_start_rz: bool = Field(False, description="Release rotation Z at start")
    
    release_end_x: bool = Field(False, description="Release translation X at end")
    release_end_y: bool = Field(False, description="Release translation Y at end")
    release_end_z: bool = Field(False, description="Release translation Z at end")
    release_end_rx: bool = Field(False, description="Release rotation X at end")
    release_end_ry: bool = Field(False, description="Release rotation Y at end")
    release_end_rz: bool = Field(False, description="Release rotation Z at end")


class ElementCreate(ElementBase):
    """
    Schema for creating a new element.
    """
    project_id: str = Field(..., description="Project ID")


class ElementUpdate(BaseModel):
    """
    Schema for updating an existing element.
    """
    name: Optional[str] = Field(None, description="Element name or identifier")
    element_type: Optional[ElementType] = Field(None, description="Element type")
    start_node_id: Optional[str] = Field(None, description="Start node ID")
    end_node_id: Optional[str] = Field(None, description="End node ID")
    section_id: Optional[str] = Field(None, description="Section ID")
    material_id: Optional[str] = Field(None, description="Material ID")
    angle: Optional[float] = Field(None, description="Rotation angle in degrees")
    
    # Release conditions
    release_start_x: Optional[bool] = Field(None, description="Release translation X at start")
    release_start_y: Optional[bool] = Field(None, description="Release translation Y at start")
    release_start_z: Optional[bool] = Field(None, description="Release translation Z at start")
    release_start_rx: Optional[bool] = Field(None, description="Release rotation X at start")
    release_start_ry: Optional[bool] = Field(None, description="Release rotation Y at start")
    release_start_rz: Optional[bool] = Field(None, description="Release rotation Z at start")
    
    release_end_x: Optional[bool] = Field(None, description="Release translation X at end")
    release_end_y: Optional[bool] = Field(None, description="Release translation Y at end")
    release_end_z: Optional[bool] = Field(None, description="Release translation Z at end")
    release_end_rx: Optional[bool] = Field(None, description="Release rotation X at end")
    release_end_ry: Optional[bool] = Field(None, description="Release rotation Y at end")
    release_end_rz: Optional[bool] = Field(None, description="Release rotation Z at end")


class ElementResponse(ElementBase, BaseSchema):
    """
    Schema for element response.
    """
    project_id: str = Field(..., description="Project ID")
    length: float = Field(..., description="Element length (m)")


class ElementDetail(ElementResponse):
    """
    Schema for detailed element response.
    """
    start_node: Dict[str, Any] = Field(..., description="Start node details")
    end_node: Dict[str, Any] = Field(..., description="End node details")
    section: Dict[str, Any] = Field(..., description="Section details")
    material: Dict[str, Any] = Field(..., description="Material details")