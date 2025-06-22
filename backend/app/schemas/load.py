from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.models.load import LoadType
from app.schemas.base import BaseSchema


class LoadCaseBase(BaseModel):
    """
    Base schema for load case data.
    """
    name: str = Field(..., description="Load case name")
    description: Optional[str] = Field(None, description="Load case description")
    is_active: bool = Field(True, description="Whether the load case is active")


class LoadCaseCreate(LoadCaseBase):
    """
    Schema for creating a new load case.
    """
    project_id: str = Field(..., description="Project ID")


class LoadCaseUpdate(BaseModel):
    """
    Schema for updating an existing load case.
    """
    name: Optional[str] = Field(None, description="Load case name")
    description: Optional[str] = Field(None, description="Load case description")
    is_active: Optional[bool] = Field(None, description="Whether the load case is active")


class LoadCaseResponse(LoadCaseBase, BaseSchema):
    """
    Schema for load case response.
    """
    project_id: str = Field(..., description="Project ID")
    load_count: int = Field(0, description="Number of loads in the load case")


class LoadCombinationBase(BaseModel):
    """
    Base schema for load combination data.
    """
    name: str = Field(..., description="Load combination name")
    description: Optional[str] = Field(None, description="Load combination description")
    is_active: bool = Field(True, description="Whether the load combination is active")


class LoadCombinationCreate(LoadCombinationBase):
    """
    Schema for creating a new load combination.
    """
    project_id: str = Field(..., description="Project ID")
    load_cases: List[Dict[str, Any]] = Field(..., description="List of load cases with factors")


class LoadCombinationUpdate(BaseModel):
    """
    Schema for updating an existing load combination.
    """
    name: Optional[str] = Field(None, description="Load combination name")
    description: Optional[str] = Field(None, description="Load combination description")
    is_active: Optional[bool] = Field(None, description="Whether the load combination is active")
    load_cases: Optional[List[Dict[str, Any]]] = Field(None, description="List of load cases with factors")


class LoadCombinationResponse(LoadCombinationBase, BaseSchema):
    """
    Schema for load combination response.
    """
    project_id: str = Field(..., description="Project ID")
    load_cases: List[Dict[str, Any]] = Field(..., description="List of load cases with factors")


class LoadBase(BaseModel):
    """
    Base schema for load data.
    """
    load_case_id: str = Field(..., description="Load case ID")
    load_type: LoadType = Field(..., description="Load type")
    
    # Target (either node or element)
    node_id: Optional[str] = Field(None, description="Node ID (for point loads)")
    element_id: Optional[str] = Field(None, description="Element ID (for distributed loads)")
    
    # Load values
    fx: Optional[float] = Field(None, description="Force in X direction (N)")
    fy: Optional[float] = Field(None, description="Force in Y direction (N)")
    fz: Optional[float] = Field(None, description="Force in Z direction (N)")
    mx: Optional[float] = Field(None, description="Moment around X axis (N·m)")
    my: Optional[float] = Field(None, description="Moment around Y axis (N·m)")
    mz: Optional[float] = Field(None, description="Moment around Z axis (N·m)")
    
    # For distributed loads
    start_distance: Optional[float] = Field(None, description="Distance from start node (m)")
    end_distance: Optional[float] = Field(None, description="Distance from start node (m)")
    
    # For temperature loads
    temperature_change: Optional[float] = Field(None, description="Temperature change (°C)")
    temperature_gradient: Optional[float] = Field(None, description="Temperature gradient (°C/m)")


class LoadCreate(LoadBase):
    """
    Schema for creating a new load.
    """
    project_id: str = Field(..., description="Project ID")


class LoadUpdate(BaseModel):
    """
    Schema for updating an existing load.
    """
    load_case_id: Optional[str] = Field(None, description="Load case ID")
    load_type: Optional[LoadType] = Field(None, description="Load type")
    
    # Target (either node or element)
    node_id: Optional[str] = Field(None, description="Node ID (for point loads)")
    element_id: Optional[str] = Field(None, description="Element ID (for distributed loads)")
    
    # Load values
    fx: Optional[float] = Field(None, description="Force in X direction (N)")
    fy: Optional[float] = Field(None, description="Force in Y direction (N)")
    fz: Optional[float] = Field(None, description="Force in Z direction (N)")
    mx: Optional[float] = Field(None, description="Moment around X axis (N·m)")
    my: Optional[float] = Field(None, description="Moment around Y axis (N·m)")
    mz: Optional[float] = Field(None, description="Moment around Z axis (N·m)")
    
    # For distributed loads
    start_distance: Optional[float] = Field(None, description="Distance from start node (m)")
    end_distance: Optional[float] = Field(None, description="Distance from start node (m)")
    
    # For temperature loads
    temperature_change: Optional[float] = Field(None, description="Temperature change (°C)")
    temperature_gradient: Optional[float] = Field(None, description="Temperature gradient (°C/m)")


class LoadResponse(LoadBase, BaseSchema):
    """
    Schema for load response.
    """
    project_id: str = Field(..., description="Project ID")