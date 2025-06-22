from sqlalchemy import Column, String, Float, ForeignKey, Integer, Enum, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.models.base import BaseModel


class AnalysisType(str, enum.Enum):
    LINEAR_STATIC = "linear_static"
    NONLINEAR_STATIC = "nonlinear_static"
    MODAL = "modal"
    RESPONSE_SPECTRUM = "response_spectrum"
    TIME_HISTORY = "time_history"
    BUCKLING = "buckling"
    P_DELTA = "p_delta"


class Analysis(BaseModel):
    """
    Analysis model for storing analysis configurations and results.
    """
    project_id = Column(String(36), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    analysis_type = Column(Enum(AnalysisType), nullable=False)
    
    # Analysis options
    include_p_delta = Column(Boolean, default=False)
    include_large_deformation = Column(Boolean, default=False)
    include_shear_deformation = Column(Boolean, default=True)
    
    # Load cases/combinations to analyze
    load_case_ids = Column(JSON, nullable=True)  # List of load case IDs
    load_combination_ids = Column(JSON, nullable=True)  # List of load combination IDs
    
    # Analysis status
    is_complete = Column(Boolean, default=False)
    run_date = Column(DateTime, nullable=True)
    
    # For modal analysis
    num_modes = Column(Integer, nullable=True)
    
    # For time history analysis
    time_step = Column(Float, nullable=True)
    num_steps = Column(Integer, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="analyses")
    node_results = relationship("NodeResult", back_populates="analysis", cascade="all, delete-orphan")
    element_results = relationship("ElementResult", back_populates="analysis", cascade="all, delete-orphan")
    modal_results = relationship("ModalResult", back_populates="analysis", cascade="all, delete-orphan")


class NodeResult(BaseModel):
    """
    Node result model for storing analysis results at nodes.
    """
    analysis_id = Column(String(36), ForeignKey("analysis.id", ondelete="CASCADE"), nullable=False)
    node_id = Column(String(36), ForeignKey("node.id", ondelete="CASCADE"), nullable=False)
    load_case_id = Column(String(36), ForeignKey("loadcase.id", ondelete="CASCADE"), nullable=True)
    load_combination_id = Column(String(36), ForeignKey("loadcombination.id", ondelete="CASCADE"), nullable=True)
    
    # Displacements
    dx = Column(Float, nullable=True)  # mm
    dy = Column(Float, nullable=True)  # mm
    dz = Column(Float, nullable=True)  # mm
    rx = Column(Float, nullable=True)  # rad
    ry = Column(Float, nullable=True)  # rad
    rz = Column(Float, nullable=True)  # rad
    
    # Reactions (if node is a support)
    fx = Column(Float, nullable=True)  # N
    fy = Column(Float, nullable=True)  # N
    fz = Column(Float, nullable=True)  # N
    mx = Column(Float, nullable=True)  # N·m
    my = Column(Float, nullable=True)  # N·m
    mz = Column(Float, nullable=True)  # N·m
    
    # Relationships
    analysis = relationship("Analysis", back_populates="node_results")
    node = relationship("Node")
    load_case = relationship("LoadCase", foreign_keys=[load_case_id])
    load_combination = relationship("LoadCombination", foreign_keys=[load_combination_id])


class ElementResult(BaseModel):
    """
    Element result model for storing analysis results for elements.
    """
    analysis_id = Column(String(36), ForeignKey("analysis.id", ondelete="CASCADE"), nullable=False)
    element_id = Column(String(36), ForeignKey("element.id", ondelete="CASCADE"), nullable=False)
    load_case_id = Column(String(36), ForeignKey("loadcase.id", ondelete="CASCADE"), nullable=True)
    load_combination_id = Column(String(36), ForeignKey("loadcombination.id", ondelete="CASCADE"), nullable=True)
    
    # Position along element (0.0 to 1.0)
    position = Column(Float, nullable=False)
    
    # Forces and moments
    axial_force = Column(Float, nullable=True)  # N
    shear_force_y = Column(Float, nullable=True)  # N
    shear_force_z = Column(Float, nullable=True)  # N
    torsional_moment = Column(Float, nullable=True)  # N·m
    bending_moment_y = Column(Float, nullable=True)  # N·m
    bending_moment_z = Column(Float, nullable=True)  # N·m
    
    # Stresses
    axial_stress = Column(Float, nullable=True)  # MPa
    bending_stress_y = Column(Float, nullable=True)  # MPa
    bending_stress_z = Column(Float, nullable=True)  # MPa
    shear_stress_y = Column(Float, nullable=True)  # MPa
    shear_stress_z = Column(Float, nullable=True)  # MPa
    von_mises_stress = Column(Float, nullable=True)  # MPa
    
    # Relationships
    analysis = relationship("Analysis", back_populates="element_results")
    element = relationship("Element", back_populates="analysis_results")
    load_case = relationship("LoadCase", foreign_keys=[load_case_id])
    load_combination = relationship("LoadCombination", foreign_keys=[load_combination_id])


class ModalResult(BaseModel):
    """
    Modal result model for storing modal analysis results.
    """
    analysis_id = Column(String(36), ForeignKey("analysis.id", ondelete="CASCADE"), nullable=False)
    
    # Modal properties
    mode_number = Column(Integer, nullable=False)
    frequency = Column(Float, nullable=False)  # Hz
    period = Column(Float, nullable=False)  # s
    modal_mass = Column(Float, nullable=False)  # kg
    
    # Modal participation factors
    participation_x = Column(Float, nullable=True)
    participation_y = Column(Float, nullable=True)
    participation_z = Column(Float, nullable=True)
    participation_rx = Column(Float, nullable=True)
    participation_ry = Column(Float, nullable=True)
    participation_rz = Column(Float, nullable=True)
    
    # Mode shape data (stored as JSON)
    mode_shape = Column(JSON, nullable=True)  # {node_id: [dx, dy, dz, rx, ry, rz], ...}
    
    # Relationships
    analysis = relationship("Analysis", back_populates="modal_results")