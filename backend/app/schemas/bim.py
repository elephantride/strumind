from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class BIMModelBase(BaseModel):
    """
    Base schema for BIM model data.
    """
    project_id: str = Field(..., description="Project ID")
    name: str = Field(..., description="BIM model name")
    description: Optional[str] = Field(None, description="BIM model description")


class BIMModelCreate(BIMModelBase):
    """
    Schema for creating a new BIM model.
    """
    pass


class BIMModelUpdate(BaseModel):
    """
    Schema for updating an existing BIM model.
    """
    name: Optional[str] = Field(None, description="BIM model name")
    description: Optional[str] = Field(None, description="BIM model description")


class BIMModelResponse(BIMModelBase, BaseSchema):
    """
    Schema for BIM model response.
    """
    pass


class BIMGeometryBase(BaseModel):
    """
    Base schema for BIM geometry data.
    """
    element_id: str = Field(..., description="Element ID")
    geometry_type: str = Field(..., description="Geometry type (beam, column, slab, etc.)")
    vertices: List[List[float]] = Field(..., description="List of vertex coordinates [x, y, z]")
    faces: Optional[List[List[int]]] = Field(None, description="List of faces (indices of vertices)")
    edges: Optional[List[List[int]]] = Field(None, description="List of edges (indices of vertices)")
    
    # Appearance
    color: Optional[str] = Field(None, description="Color in hex format (#RRGGBB)")
    opacity: Optional[float] = Field(1.0, description="Opacity (0.0 to 1.0)")
    
    # Metadata
    properties: Optional[Dict[str, Any]] = Field(None, description="Additional properties")


class BIMGeometryCreate(BIMGeometryBase):
    """
    Schema for creating new BIM geometry.
    """
    project_id: str = Field(..., description="Project ID")
    bim_model_id: str = Field(..., description="BIM model ID")


class BIMGeometryUpdate(BaseModel):
    """
    Schema for updating existing BIM geometry.
    """
    vertices: Optional[List[List[float]]] = Field(None, description="List of vertex coordinates [x, y, z]")
    faces: Optional[List[List[int]]] = Field(None, description="List of faces (indices of vertices)")
    edges: Optional[List[List[int]]] = Field(None, description="List of edges (indices of vertices)")
    
    # Appearance
    color: Optional[str] = Field(None, description="Color in hex format (#RRGGBB)")
    opacity: Optional[float] = Field(None, description="Opacity (0.0 to 1.0)")
    
    # Metadata
    properties: Optional[Dict[str, Any]] = Field(None, description="Additional properties")


class BIMGeometryResponse(BIMGeometryBase, BaseSchema):
    """
    Schema for BIM geometry response.
    """
    project_id: str = Field(..., description="Project ID")
    bim_model_id: str = Field(..., description="BIM model ID")


class BIMViewerData(BaseModel):
    """
    Schema for BIM viewer data.
    """
    project_id: str = Field(..., description="Project ID")
    model_name: str = Field(..., description="Model name")
    elements: List[Dict[str, Any]] = Field(..., description="List of elements with geometry")
    materials: Optional[List[Dict[str, Any]]] = Field(None, description="List of materials")
    camera_position: Optional[List[float]] = Field(None, description="Camera position [x, y, z]")
    target_position: Optional[List[float]] = Field(None, description="Camera target position [x, y, z]")