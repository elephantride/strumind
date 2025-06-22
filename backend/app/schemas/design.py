from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.design import DesignCode, DesignMethod
from app.schemas.base import BaseSchema


class DesignBase(BaseModel):
    """
    Base schema for design data.
    """
    name: str = Field(..., description="Design name")
    design_code: DesignCode = Field(..., description="Design code")
    design_method: DesignMethod = Field(..., description="Design method")
    
    # Analysis to use for design
    analysis_id: str = Field(..., description="Analysis ID")
    
    # Design options
    load_combination_ids: Optional[List[str]] = Field(None, description="List of load combination IDs to consider")


class DesignCreate(DesignBase):
    """
    Schema for creating a new design.
    """
    project_id: str = Field(..., description="Project ID")


class DesignUpdate(BaseModel):
    """
    Schema for updating an existing design.
    """
    name: Optional[str] = Field(None, description="Design name")
    design_code: Optional[DesignCode] = Field(None, description="Design code")
    design_method: Optional[DesignMethod] = Field(None, description="Design method")
    
    # Analysis to use for design
    analysis_id: Optional[str] = Field(None, description="Analysis ID")
    
    # Design options
    load_combination_ids: Optional[List[str]] = Field(None, description="List of load combination IDs to consider")


class DesignResponse(DesignBase, BaseSchema):
    """
    Schema for design response.
    """
    project_id: str = Field(..., description="Project ID")
    is_complete: bool = Field(False, description="Whether the design is complete")
    run_date: Optional[datetime] = Field(None, description="Date and time of design run")
    
    # Design summary
    elements_passed: Optional[int] = Field(None, description="Number of elements that passed")
    elements_warning: Optional[int] = Field(None, description="Number of elements with warnings")
    elements_failed: Optional[int] = Field(None, description="Number of elements that failed")
    max_unity_ratio: Optional[float] = Field(None, description="Maximum unity ratio")


class DesignRunRequest(BaseModel):
    """
    Schema for running a design.
    """
    design_id: str = Field(..., description="Design ID")


class ElementDesignResultResponse(BaseSchema):
    """
    Schema for element design result response.
    """
    design_id: str = Field(..., description="Design ID")
    element_id: str = Field(..., description="Element ID")
    
    # Design status
    status: str = Field(..., description="Design status (pass, warning, fail)")
    
    # Design checks
    axial_check: Optional[float] = Field(None, description="Axial check ratio")
    flexural_check: Optional[float] = Field(None, description="Flexural check ratio")
    shear_check: Optional[float] = Field(None, description="Shear check ratio")
    torsion_check: Optional[float] = Field(None, description="Torsion check ratio")
    combined_check: Optional[float] = Field(None, description="Combined check ratio (unity)")
    
    # Governing equation/condition
    governing_equation: Optional[str] = Field(None, description="Governing equation or condition")
    
    # Detailed design data
    design_details: Optional[Dict[str, Any]] = Field(None, description="Detailed design data")
    
    # Optimization suggestions
    suggested_section_id: Optional[str] = Field(None, description="Suggested section ID")
    suggested_section: Optional[Dict[str, Any]] = Field(None, description="Suggested section details")