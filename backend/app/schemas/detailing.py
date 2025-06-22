from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class DetailingBase(BaseModel):
    """
    Base schema for detailing data.
    """
    project_id: str = Field(..., description="Project ID")
    name: str = Field(..., description="Detailing name")
    description: Optional[str] = Field(None, description="Detailing description")
    
    # Design to use for detailing
    design_id: str = Field(..., description="Design ID")
    
    # Detailing options
    element_ids: Optional[List[str]] = Field(None, description="List of element IDs to detail")
    detailing_options: Optional[Dict[str, Any]] = Field(None, description="Detailing options")


class DetailingCreate(DetailingBase):
    """
    Schema for creating a new detailing.
    """
    pass


class DetailingUpdate(BaseModel):
    """
    Schema for updating an existing detailing.
    """
    name: Optional[str] = Field(None, description="Detailing name")
    description: Optional[str] = Field(None, description="Detailing description")
    
    # Design to use for detailing
    design_id: Optional[str] = Field(None, description="Design ID")
    
    # Detailing options
    element_ids: Optional[List[str]] = Field(None, description="List of element IDs to detail")
    detailing_options: Optional[Dict[str, Any]] = Field(None, description="Detailing options")


class DetailingResponse(DetailingBase, BaseSchema):
    """
    Schema for detailing response.
    """
    is_complete: bool = Field(False, description="Whether the detailing is complete")


class DetailingRunRequest(BaseModel):
    """
    Schema for running a detailing.
    """
    detailing_id: str = Field(..., description="Detailing ID")


class ElementDetailingBase(BaseModel):
    """
    Base schema for element detailing data.
    """
    detailing_id: str = Field(..., description="Detailing ID")
    element_id: str = Field(..., description="Element ID")
    
    # Detailing data
    detail_type: str = Field(..., description="Detail type (connection, reinforcement, etc.)")
    detail_data: Dict[str, Any] = Field(..., description="Detail data")
    
    # Drawing data
    drawing_data: Optional[Dict[str, Any]] = Field(None, description="Drawing data")
    
    # Fabrication data
    fabrication_data: Optional[Dict[str, Any]] = Field(None, description="Fabrication data")


class ElementDetailingCreate(ElementDetailingBase):
    """
    Schema for creating new element detailing.
    """
    project_id: str = Field(..., description="Project ID")


class ElementDetailingUpdate(BaseModel):
    """
    Schema for updating existing element detailing.
    """
    detail_data: Optional[Dict[str, Any]] = Field(None, description="Detail data")
    drawing_data: Optional[Dict[str, Any]] = Field(None, description="Drawing data")
    fabrication_data: Optional[Dict[str, Any]] = Field(None, description="Fabrication data")


class ElementDetailingResponse(ElementDetailingBase, BaseSchema):
    """
    Schema for element detailing response.
    """
    project_id: str = Field(..., description="Project ID")


class ConnectionDetailBase(BaseModel):
    """
    Base schema for connection detail data.
    """
    element_detailing_id: str = Field(..., description="Element detailing ID")
    connection_type: str = Field(..., description="Connection type")
    
    # Connection data
    connection_data: Dict[str, Any] = Field(..., description="Connection data")
    
    # Bolts, welds, plates, etc.
    bolts: Optional[List[Dict[str, Any]]] = Field(None, description="Bolt data")
    welds: Optional[List[Dict[str, Any]]] = Field(None, description="Weld data")
    plates: Optional[List[Dict[str, Any]]] = Field(None, description="Plate data")
    
    # Geometry
    geometry: Optional[Dict[str, Any]] = Field(None, description="Connection geometry")


class ConnectionDetailCreate(ConnectionDetailBase):
    """
    Schema for creating a new connection detail.
    """
    project_id: str = Field(..., description="Project ID")


class ConnectionDetailUpdate(BaseModel):
    """
    Schema for updating an existing connection detail.
    """
    connection_data: Optional[Dict[str, Any]] = Field(None, description="Connection data")
    bolts: Optional[List[Dict[str, Any]]] = Field(None, description="Bolt data")
    welds: Optional[List[Dict[str, Any]]] = Field(None, description="Weld data")
    plates: Optional[List[Dict[str, Any]]] = Field(None, description="Plate data")
    geometry: Optional[Dict[str, Any]] = Field(None, description="Connection geometry")


class ConnectionDetailResponse(ConnectionDetailBase, BaseSchema):
    """
    Schema for connection detail response.
    """
    project_id: str = Field(..., description="Project ID")