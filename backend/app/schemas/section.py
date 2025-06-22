from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.models.section import SectionType
from app.schemas.base import BaseSchema


class SectionBase(BaseModel):
    """
    Base schema for section data.
    """
    name: str = Field(..., description="Section name")
    section_type: SectionType = Field(..., description="Section type")
    material_id: str = Field(..., description="Material ID")
    
    # Section properties
    area: float = Field(..., description="Cross-sectional area (mm²)")
    moment_of_inertia_y: float = Field(..., description="Moment of inertia about y-axis (mm⁴)")
    moment_of_inertia_z: float = Field(..., description="Moment of inertia about z-axis (mm⁴)")
    torsional_constant: float = Field(..., description="Torsional constant (mm⁴)")
    
    # Section modulus
    elastic_modulus_y: float = Field(..., description="Elastic section modulus about y-axis (mm³)")
    elastic_modulus_z: float = Field(..., description="Elastic section modulus about z-axis (mm³)")
    plastic_modulus_y: Optional[float] = Field(None, description="Plastic section modulus about y-axis (mm³)")
    plastic_modulus_z: Optional[float] = Field(None, description="Plastic section modulus about z-axis (mm³)")
    
    # Radius of gyration
    radius_of_gyration_y: Optional[float] = Field(None, description="Radius of gyration about y-axis (mm)")
    radius_of_gyration_z: Optional[float] = Field(None, description="Radius of gyration about z-axis (mm)")
    
    # Dimensions (specific to section type)
    dimensions: Optional[Dict[str, Any]] = Field(None, description="Section dimensions")


class SectionCreate(SectionBase):
    """
    Schema for creating a new section.
    """
    project_id: str = Field(..., description="Project ID")


class SectionUpdate(BaseModel):
    """
    Schema for updating an existing section.
    """
    name: Optional[str] = Field(None, description="Section name")
    section_type: Optional[SectionType] = Field(None, description="Section type")
    material_id: Optional[str] = Field(None, description="Material ID")
    
    # Section properties
    area: Optional[float] = Field(None, description="Cross-sectional area (mm²)")
    moment_of_inertia_y: Optional[float] = Field(None, description="Moment of inertia about y-axis (mm⁴)")
    moment_of_inertia_z: Optional[float] = Field(None, description="Moment of inertia about z-axis (mm⁴)")
    torsional_constant: Optional[float] = Field(None, description="Torsional constant (mm⁴)")
    
    # Section modulus
    elastic_modulus_y: Optional[float] = Field(None, description="Elastic section modulus about y-axis (mm³)")
    elastic_modulus_z: Optional[float] = Field(None, description="Elastic section modulus about z-axis (mm³)")
    plastic_modulus_y: Optional[float] = Field(None, description="Plastic section modulus about y-axis (mm³)")
    plastic_modulus_z: Optional[float] = Field(None, description="Plastic section modulus about z-axis (mm³)")
    
    # Radius of gyration
    radius_of_gyration_y: Optional[float] = Field(None, description="Radius of gyration about y-axis (mm)")
    radius_of_gyration_z: Optional[float] = Field(None, description="Radius of gyration about z-axis (mm)")
    
    # Dimensions (specific to section type)
    dimensions: Optional[Dict[str, Any]] = Field(None, description="Section dimensions")


class SectionResponse(SectionBase, BaseSchema):
    """
    Schema for section response.
    """
    project_id: str = Field(..., description="Project ID")