from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Node(BaseModel):
    """
    Node model for storing structural nodes.
    """
    project_id = Column(String(36), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    
    # Support conditions
    is_support = Column(Boolean, default=False)
    restraint_x = Column(Boolean, default=False)
    restraint_y = Column(Boolean, default=False)
    restraint_z = Column(Boolean, default=False)
    restraint_rx = Column(Boolean, default=False)
    restraint_ry = Column(Boolean, default=False)
    restraint_rz = Column(Boolean, default=False)
    
    # Spring stiffness (if applicable)
    spring_x = Column(Float, nullable=True)
    spring_y = Column(Float, nullable=True)
    spring_z = Column(Float, nullable=True)
    spring_rx = Column(Float, nullable=True)
    spring_ry = Column(Float, nullable=True)
    spring_rz = Column(Float, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="nodes")
    elements_start = relationship("Element", foreign_keys="Element.start_node_id", back_populates="start_node")
    elements_end = relationship("Element", foreign_keys="Element.end_node_id", back_populates="end_node")
    loads = relationship("Load", back_populates="node")