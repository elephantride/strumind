import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.element import Element
from app.models.node import Node
from app.models.material import Material
from app.models.section import Section
from app.models.project import Project
from app.core.bim.geometry import generate_bim_geometry

logger = logging.getLogger(__name__)


def get_bim_viewer_data(
    db: Session, 
    project_id: str, 
    model_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get BIM viewer data for a project.
    """
    try:
        # Get project
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")
        
        # Get elements
        elements = db.query(Element).filter(Element.project_id == project_id).all()
        
        # Get materials
        materials = db.query(Material).filter(Material.project_id == project_id).all()
        
        # Generate geometry for all elements
        geometries = generate_bim_geometry(db, project_id, model_id or "default")
        
        # Prepare materials data
        materials_data = []
        for material in materials:
            materials_data.append({
                "id": material.id,
                "name": material.name,
                "type": material.material_type,
                "color": _get_material_color(material),
                "properties": {
                    "elastic_modulus": material.elastic_modulus,
                    "poisson_ratio": material.poisson_ratio,
                    "density": material.density,
                    "yield_strength": material.yield_strength,
                    "ultimate_strength": material.ultimate_strength
                }
            })
        
        # Prepare camera position
        # Default to a position that shows the entire model
        # In a real implementation, this would be calculated based on the model bounds
        camera_position = [10, 10, 10]
        target_position = [0, 0, 0]
        
        # Return viewer data
        return {
            "project_id": project_id,
            "model_name": project.name,
            "elements": geometries,
            "materials": materials_data,
            "camera_position": camera_position,
            "target_position": target_position
        }
    
    except Exception as e:
        logger.error(f"Error getting BIM viewer data: {str(e)}")
        # Return empty data
        return {
            "project_id": project_id,
            "model_name": "Error",
            "elements": [],
            "materials": [],
            "camera_position": [10, 10, 10],
            "target_position": [0, 0, 0]
        }


def _get_material_color(material: Material) -> str:
    """
    Get color for a material based on its type.
    """
    if material.material_type == "STEEL":
        return "#9E9E9E"  # Grey
    elif material.material_type == "CONCRETE":
        return "#BDBDBD"  # Light grey
    elif material.material_type == "TIMBER":
        return "#8D6E63"  # Brown
    elif material.material_type == "ALUMINUM":
        return "#E0E0E0"  # Silver
    else:
        return "#9E9E9E"  # Grey