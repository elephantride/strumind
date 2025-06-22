from sqlalchemy import Column, String, Float, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class MaterialType(str, enum.Enum):
    STEEL = "steel"
    CONCRETE = "concrete"
    TIMBER = "timber"
    ALUMINUM = "aluminum"
    COMPOSITE = "composite"
    CUSTOM = "custom"


class Material(BaseModel):
    """
    Material model for storing structural materials.
    """
    project_id = Column(String(36), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    material_type = Column(Enum(MaterialType), nullable=False)
    
    # Common material properties
    density = Column(Float, nullable=False)  # kg/m³
    elastic_modulus = Column(Float, nullable=False)  # MPa
    poisson_ratio = Column(Float, nullable=False)
    thermal_coefficient = Column(Float, nullable=True)  # 1/°C
    
    # Strength properties
    yield_strength = Column(Float, nullable=True)  # MPa
    ultimate_strength = Column(Float, nullable=True)  # MPa
    
    # Concrete specific properties
    compressive_strength = Column(Float, nullable=True)  # MPa
    tensile_strength = Column(Float, nullable=True)  # MPa
    
    # Relationships
    project = relationship("Project", back_populates="materials")
    elements = relationship("Element", back_populates="material")
    sections = relationship("Section", back_populates="material")