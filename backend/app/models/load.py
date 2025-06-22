from sqlalchemy import Column, String, Float, ForeignKey, Integer, Enum, Boolean
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class LoadType(str, enum.Enum):
    POINT = "point"
    DISTRIBUTED = "distributed"
    MOMENT = "moment"
    TEMPERATURE = "temperature"
    SETTLEMENT = "settlement"
    PRESTRESS = "prestress"


class LoadCase(BaseModel):
    """
    Load case model for grouping loads.
    """
    project_id = Column(String(36), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    project = relationship("Project", back_populates="load_cases")
    loads = relationship("Load", back_populates="load_case", cascade="all, delete-orphan")
    load_combinations = relationship("LoadCombinationCase", back_populates="load_case")


class LoadCombination(BaseModel):
    """
    Load combination model for combining load cases.
    """
    project_id = Column(String(36), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    project = relationship("Project", back_populates="load_combinations")
    load_cases = relationship("LoadCombinationCase", back_populates="load_combination", cascade="all, delete-orphan")


class LoadCombinationCase(BaseModel):
    """
    Junction table for load combinations and load cases.
    """
    load_combination_id = Column(String(36), ForeignKey("loadcombination.id", ondelete="CASCADE"), nullable=False)
    load_case_id = Column(String(36), ForeignKey("loadcase.id", ondelete="CASCADE"), nullable=False)
    factor = Column(Float, nullable=False, default=1.0)
    
    # Relationships
    load_combination = relationship("LoadCombination", back_populates="load_cases")
    load_case = relationship("LoadCase", back_populates="load_combinations")


class Load(BaseModel):
    """
    Load model for storing structural loads.
    """
    project_id = Column(String(36), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    load_case_id = Column(String(36), ForeignKey("loadcase.id", ondelete="CASCADE"), nullable=False)
    load_type = Column(Enum(LoadType), nullable=False)
    
    # Target (either node or element)
    node_id = Column(String(36), ForeignKey("node.id", ondelete="CASCADE"), nullable=True)
    element_id = Column(String(36), ForeignKey("element.id", ondelete="CASCADE"), nullable=True)
    
    # Load values
    fx = Column(Float, nullable=True)  # Force in X direction (N)
    fy = Column(Float, nullable=True)  # Force in Y direction (N)
    fz = Column(Float, nullable=True)  # Force in Z direction (N)
    mx = Column(Float, nullable=True)  # Moment around X axis (N·m)
    my = Column(Float, nullable=True)  # Moment around Y axis (N·m)
    mz = Column(Float, nullable=True)  # Moment around Z axis (N·m)
    
    # For distributed loads
    start_distance = Column(Float, nullable=True)  # Distance from start node (m)
    end_distance = Column(Float, nullable=True)  # Distance from start node (m)
    
    # For temperature loads
    temperature_change = Column(Float, nullable=True)  # °C
    temperature_gradient = Column(Float, nullable=True)  # °C/m
    
    # Relationships
    project = relationship("Project", back_populates="loads")
    load_case = relationship("LoadCase", back_populates="loads")
    node = relationship("Node", back_populates="loads")
    element = relationship("Element", back_populates="loads")