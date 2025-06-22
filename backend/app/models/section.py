from sqlalchemy import Column, String, Float, ForeignKey, Integer, Enum, JSON
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class SectionType(str, enum.Enum):
    I_SECTION = "i_section"
    H_SECTION = "h_section"
    CHANNEL = "channel"
    ANGLE = "angle"
    TEE = "tee"
    RECTANGULAR_HOLLOW = "rectangular_hollow"
    CIRCULAR_HOLLOW = "circular_hollow"
    RECTANGULAR = "rectangular"
    CIRCULAR = "circular"
    CUSTOM = "custom"


class Section(BaseModel):
    """
    Section model for storing structural sections.
    """
    project_id = Column(String(36), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    section_type = Column(Enum(SectionType), nullable=False)
    material_id = Column(String(36), ForeignKey("material.id"), nullable=False)
    
    # Section properties
    area = Column(Float, nullable=False)  # mm²
    
    # Moment of inertia
    moment_of_inertia_y = Column(Float, nullable=False)  # mm⁴
    moment_of_inertia_z = Column(Float, nullable=False)  # mm⁴
    torsional_constant = Column(Float, nullable=False)  # mm⁴
    
    # Section modulus
    elastic_modulus_y = Column(Float, nullable=False)  # mm³
    elastic_modulus_z = Column(Float, nullable=False)  # mm³
    plastic_modulus_y = Column(Float, nullable=True)  # mm³
    plastic_modulus_z = Column(Float, nullable=True)  # mm³
    
    # Radius of gyration
    radius_of_gyration_y = Column(Float, nullable=True)  # mm
    radius_of_gyration_z = Column(Float, nullable=True)  # mm
    
    # Dimensions (specific to section type)
    dimensions = Column(JSON, nullable=True)  # Store dimensions based on section type
    
    # Relationships
    project = relationship("Project", back_populates="sections")
    material = relationship("Material", back_populates="sections")
    elements = relationship("Element", back_populates="section")