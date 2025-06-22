from sqlalchemy import Column, String, Float, ForeignKey, Integer, Enum, Boolean
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class ElementType(str, enum.Enum):
    BEAM = "beam"
    COLUMN = "column"
    BRACE = "brace"
    TRUSS = "truss"
    SHELL = "shell"
    PLATE = "plate"
    SOLID = "solid"


class Element(BaseModel):
    """
    Element model for storing structural elements.
    """
    project_id = Column(String(36), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    element_type = Column(Enum(ElementType), nullable=False)
    
    # Connectivity
    start_node_id = Column(String(36), ForeignKey("node.id", ondelete="CASCADE"), nullable=False)
    end_node_id = Column(String(36), ForeignKey("node.id", ondelete="CASCADE"), nullable=False)
    
    # Properties
    section_id = Column(String(36), ForeignKey("section.id", ondelete="CASCADE"), nullable=False)
    material_id = Column(String(36), ForeignKey("material.id", ondelete="CASCADE"), nullable=False)
    
    # Orientation
    angle = Column(Float, default=0.0)  # Rotation angle in degrees
    
    # Release conditions (for frame elements)
    release_start_x = Column(Boolean, default=False)
    release_start_y = Column(Boolean, default=False)
    release_start_z = Column(Boolean, default=False)
    release_start_rx = Column(Boolean, default=False)
    release_start_ry = Column(Boolean, default=False)
    release_start_rz = Column(Boolean, default=False)
    
    release_end_x = Column(Boolean, default=False)
    release_end_y = Column(Boolean, default=False)
    release_end_z = Column(Boolean, default=False)
    release_end_rx = Column(Boolean, default=False)
    release_end_ry = Column(Boolean, default=False)
    release_end_rz = Column(Boolean, default=False)
    
    # Relationships
    project = relationship("Project", back_populates="elements")
    start_node = relationship("Node", foreign_keys=[start_node_id], back_populates="elements_start")
    end_node = relationship("Node", foreign_keys=[end_node_id], back_populates="elements_end")
    section = relationship("Section", back_populates="elements")
    material = relationship("Material", back_populates="elements")
    loads = relationship("Load", back_populates="element")
    analysis_results = relationship("ElementResult", back_populates="element", cascade="all, delete-orphan")
    design_results = relationship("ElementDesignResult", back_populates="element", cascade="all, delete-orphan")