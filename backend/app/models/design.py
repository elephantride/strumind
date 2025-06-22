from sqlalchemy import Column, String, Float, ForeignKey, Integer, Enum, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.models.base import BaseModel


class DesignCode(str, enum.Enum):
    AISC_360_16 = "aisc_360_16"
    EUROCODE_3 = "eurocode_3"
    EUROCODE_2 = "eurocode_2"
    ACI_318_19 = "aci_318_19"
    CSA_S16 = "csa_s16"
    CSA_A23_3 = "csa_a23_3"
    AS_4100 = "as_4100"
    AS_3600 = "as_3600"
    IS_800 = "is_800"
    IS_456 = "is_456"
    CUSTOM = "custom"


class DesignMethod(str, enum.Enum):
    LRFD = "lrfd"
    ASD = "asd"
    LIMIT_STATE = "limit_state"
    WORKING_STRESS = "working_stress"


class Design(BaseModel):
    """
    Design model for storing design configurations and results.
    """
    project_id = Column(String(36), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    design_code = Column(Enum(DesignCode), nullable=False)
    design_method = Column(Enum(DesignMethod), nullable=False)
    
    # Analysis to use for design
    analysis_id = Column(String(36), ForeignKey("analysis.id", ondelete="CASCADE"), nullable=False)
    
    # Design options
    load_combination_ids = Column(JSON, nullable=True)  # List of load combination IDs to consider
    
    # Design status
    is_complete = Column(Boolean, default=False)
    run_date = Column(DateTime, nullable=True)
    
    # Design summary
    elements_passed = Column(Integer, nullable=True)
    elements_warning = Column(Integer, nullable=True)
    elements_failed = Column(Integer, nullable=True)
    max_unity_ratio = Column(Float, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="designs")
    analysis = relationship("Analysis")
    element_design_results = relationship("ElementDesignResult", back_populates="design", cascade="all, delete-orphan")


class ElementDesignResult(BaseModel):
    """
    Element design result model for storing design results for elements.
    """
    design_id = Column(String(36), ForeignKey("design.id", ondelete="CASCADE"), nullable=False)
    element_id = Column(String(36), ForeignKey("element.id", ondelete="CASCADE"), nullable=False)
    
    # Design status
    status = Column(String(20), nullable=False)  # "pass", "warning", "fail"
    
    # Design checks
    axial_check = Column(Float, nullable=True)
    flexural_check = Column(Float, nullable=True)
    shear_check = Column(Float, nullable=True)
    torsion_check = Column(Float, nullable=True)
    combined_check = Column(Float, nullable=True)  # Unity ratio
    
    # Governing equation/condition
    governing_equation = Column(String(50), nullable=True)
    
    # Detailed design data (stored as JSON)
    design_details = Column(JSON, nullable=True)
    
    # Optimization suggestions
    suggested_section_id = Column(String(36), ForeignKey("section.id"), nullable=True)
    
    # Relationships
    design = relationship("Design", back_populates="element_design_results")
    element = relationship("Element", back_populates="design_results")
    suggested_section = relationship("Section")