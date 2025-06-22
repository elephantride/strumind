from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.material import MaterialType
from app.schemas.base import BaseSchema


class MaterialBase(BaseModel):
    """
    Base schema for material data.
    """
    name: str = Field(..., description="Material name")
    material_type: MaterialType = Field(..., description="Material type")
    density: float = Field(..., description="Density (kg/m³)")
    elastic_modulus: float = Field(..., description="Elastic modulus (MPa)")
    poisson_ratio: float = Field(..., description="Poisson's ratio")
    thermal_coefficient: Optional[float] = Field(None, description="Thermal expansion coefficient (1/°C)")
    
    # Strength properties
    yield_strength: Optional[float] = Field(None, description="Yield strength (MPa)")
    ultimate_strength: Optional[float] = Field(None, description="Ultimate strength (MPa)")
    
    # Concrete specific properties
    compressive_strength: Optional[float] = Field(None, description="Compressive strength (MPa)")
    tensile_strength: Optional[float] = Field(None, description="Tensile strength (MPa)")


class MaterialCreate(MaterialBase):
    """
    Schema for creating a new material.
    """
    project_id: str = Field(..., description="Project ID")


class MaterialUpdate(BaseModel):
    """
    Schema for updating an existing material.
    """
    name: Optional[str] = Field(None, description="Material name")
    material_type: Optional[MaterialType] = Field(None, description="Material type")
    density: Optional[float] = Field(None, description="Density (kg/m³)")
    elastic_modulus: Optional[float] = Field(None, description="Elastic modulus (MPa)")
    poisson_ratio: Optional[float] = Field(None, description="Poisson's ratio")
    thermal_coefficient: Optional[float] = Field(None, description="Thermal expansion coefficient (1/°C)")
    
    # Strength properties
    yield_strength: Optional[float] = Field(None, description="Yield strength (MPa)")
    ultimate_strength: Optional[float] = Field(None, description="Ultimate strength (MPa)")
    
    # Concrete specific properties
    compressive_strength: Optional[float] = Field(None, description="Compressive strength (MPa)")
    tensile_strength: Optional[float] = Field(None, description="Tensile strength (MPa)")


class MaterialResponse(MaterialBase, BaseSchema):
    """
    Schema for material response.
    """
    project_id: str = Field(..., description="Project ID")