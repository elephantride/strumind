from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.analysis import AnalysisType
from app.schemas.base import BaseSchema


class AnalysisBase(BaseModel):
    """
    Base schema for analysis data.
    """
    name: str = Field(..., description="Analysis name")
    analysis_type: AnalysisType = Field(..., description="Analysis type")
    
    # Analysis options
    include_p_delta: bool = Field(False, description="Include P-Delta effects")
    include_large_deformation: bool = Field(False, description="Include large deformation effects")
    include_shear_deformation: bool = Field(True, description="Include shear deformation")
    
    # Load cases/combinations to analyze
    load_case_ids: Optional[List[str]] = Field(None, description="List of load case IDs")
    load_combination_ids: Optional[List[str]] = Field(None, description="List of load combination IDs")
    
    # For modal analysis
    num_modes: Optional[int] = Field(None, description="Number of modes to calculate")
    
    # For time history analysis
    time_step: Optional[float] = Field(None, description="Time step (s)")
    num_steps: Optional[int] = Field(None, description="Number of time steps")


class AnalysisCreate(AnalysisBase):
    """
    Schema for creating a new analysis.
    """
    project_id: str = Field(..., description="Project ID")


class AnalysisUpdate(BaseModel):
    """
    Schema for updating an existing analysis.
    """
    name: Optional[str] = Field(None, description="Analysis name")
    analysis_type: Optional[AnalysisType] = Field(None, description="Analysis type")
    
    # Analysis options
    include_p_delta: Optional[bool] = Field(None, description="Include P-Delta effects")
    include_large_deformation: Optional[bool] = Field(None, description="Include large deformation effects")
    include_shear_deformation: Optional[bool] = Field(None, description="Include shear deformation")
    
    # Load cases/combinations to analyze
    load_case_ids: Optional[List[str]] = Field(None, description="List of load case IDs")
    load_combination_ids: Optional[List[str]] = Field(None, description="List of load combination IDs")
    
    # For modal analysis
    num_modes: Optional[int] = Field(None, description="Number of modes to calculate")
    
    # For time history analysis
    time_step: Optional[float] = Field(None, description="Time step (s)")
    num_steps: Optional[int] = Field(None, description="Number of time steps")


class AnalysisResponse(AnalysisBase, BaseSchema):
    """
    Schema for analysis response.
    """
    project_id: str = Field(..., description="Project ID")
    is_complete: bool = Field(False, description="Whether the analysis is complete")
    run_date: Optional[datetime] = Field(None, description="Date and time of analysis run")


class AnalysisRunRequest(BaseModel):
    """
    Schema for running an analysis.
    """
    analysis_id: str = Field(..., description="Analysis ID")


class NodeResultResponse(BaseSchema):
    """
    Schema for node result response.
    """
    analysis_id: str = Field(..., description="Analysis ID")
    node_id: str = Field(..., description="Node ID")
    load_case_id: Optional[str] = Field(None, description="Load case ID")
    load_combination_id: Optional[str] = Field(None, description="Load combination ID")
    
    # Displacements
    dx: Optional[float] = Field(None, description="Displacement in X direction (mm)")
    dy: Optional[float] = Field(None, description="Displacement in Y direction (mm)")
    dz: Optional[float] = Field(None, description="Displacement in Z direction (mm)")
    rx: Optional[float] = Field(None, description="Rotation around X axis (rad)")
    ry: Optional[float] = Field(None, description="Rotation around Y axis (rad)")
    rz: Optional[float] = Field(None, description="Rotation around Z axis (rad)")
    
    # Reactions (if node is a support)
    fx: Optional[float] = Field(None, description="Reaction force in X direction (N)")
    fy: Optional[float] = Field(None, description="Reaction force in Y direction (N)")
    fz: Optional[float] = Field(None, description="Reaction force in Z direction (N)")
    mx: Optional[float] = Field(None, description="Reaction moment around X axis (N·m)")
    my: Optional[float] = Field(None, description="Reaction moment around Y axis (N·m)")
    mz: Optional[float] = Field(None, description="Reaction moment around Z axis (N·m)")


class ElementResultResponse(BaseSchema):
    """
    Schema for element result response.
    """
    analysis_id: str = Field(..., description="Analysis ID")
    element_id: str = Field(..., description="Element ID")
    load_case_id: Optional[str] = Field(None, description="Load case ID")
    load_combination_id: Optional[str] = Field(None, description="Load combination ID")
    position: float = Field(..., description="Position along element (0.0 to 1.0)")
    
    # Forces and moments
    axial_force: Optional[float] = Field(None, description="Axial force (N)")
    shear_force_y: Optional[float] = Field(None, description="Shear force in Y direction (N)")
    shear_force_z: Optional[float] = Field(None, description="Shear force in Z direction (N)")
    torsional_moment: Optional[float] = Field(None, description="Torsional moment (N·m)")
    bending_moment_y: Optional[float] = Field(None, description="Bending moment around Y axis (N·m)")
    bending_moment_z: Optional[float] = Field(None, description="Bending moment around Z axis (N·m)")
    
    # Stresses
    axial_stress: Optional[float] = Field(None, description="Axial stress (MPa)")
    bending_stress_y: Optional[float] = Field(None, description="Bending stress about Y axis (MPa)")
    bending_stress_z: Optional[float] = Field(None, description="Bending stress about Z axis (MPa)")
    shear_stress_y: Optional[float] = Field(None, description="Shear stress in Y direction (MPa)")
    shear_stress_z: Optional[float] = Field(None, description="Shear stress in Z direction (MPa)")
    von_mises_stress: Optional[float] = Field(None, description="Von Mises stress (MPa)")


class ModalResultResponse(BaseSchema):
    """
    Schema for modal result response.
    """
    analysis_id: str = Field(..., description="Analysis ID")
    mode_number: int = Field(..., description="Mode number")
    frequency: float = Field(..., description="Natural frequency (Hz)")
    period: float = Field(..., description="Period (s)")
    modal_mass: float = Field(..., description="Modal mass (kg)")
    
    # Modal participation factors
    participation_x: Optional[float] = Field(None, description="Participation factor in X direction")
    participation_y: Optional[float] = Field(None, description="Participation factor in Y direction")
    participation_z: Optional[float] = Field(None, description="Participation factor in Z direction")
    participation_rx: Optional[float] = Field(None, description="Participation factor around X axis")
    participation_ry: Optional[float] = Field(None, description="Participation factor around Y axis")
    participation_rz: Optional[float] = Field(None, description="Participation factor around Z axis")
    
    # Mode shape data
    mode_shape: Optional[Dict[str, List[float]]] = Field(None, description="Mode shape data")