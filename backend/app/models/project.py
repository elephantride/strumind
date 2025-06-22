from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Project(BaseModel):
    """
    Project model for storing project information.
    """
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    client = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    nodes = relationship("Node", back_populates="project", cascade="all, delete-orphan")
    elements = relationship("Element", back_populates="project", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="project", cascade="all, delete-orphan")
    sections = relationship("Section", back_populates="project", cascade="all, delete-orphan")
    loads = relationship("Load", back_populates="project", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="project", cascade="all, delete-orphan")
    designs = relationship("Design", back_populates="project", cascade="all, delete-orphan")