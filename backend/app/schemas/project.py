from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class ProjectBase(BaseModel):
    """
    Base schema for project data.
    """
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    client: Optional[str] = Field(None, description="Client name")
    is_active: bool = Field(True, description="Whether the project is active")


class ProjectCreate(ProjectBase):
    """
    Schema for creating a new project.
    """
    pass


class ProjectUpdate(ProjectBase):
    """
    Schema for updating an existing project.
    """
    name: Optional[str] = Field(None, description="Project name")
    is_active: Optional[bool] = Field(None, description="Whether the project is active")


class ProjectResponse(ProjectBase, BaseSchema):
    """
    Schema for project response.
    """
    pass


class ProjectDetail(ProjectResponse):
    """
    Schema for detailed project response.
    """
    node_count: int = Field(0, description="Number of nodes in the project")
    element_count: int = Field(0, description="Number of elements in the project")
    material_count: int = Field(0, description="Number of materials in the project")
    section_count: int = Field(0, description="Number of sections in the project")
    load_case_count: int = Field(0, description="Number of load cases in the project")
    analysis_count: int = Field(0, description="Number of analyses in the project")
    design_count: int = Field(0, description="Number of designs in the project")