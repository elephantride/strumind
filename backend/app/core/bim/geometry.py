import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.element import Element, ElementType
from app.models.node import Node
from app.models.section import Section, SectionType
from app.models.material import Material

logger = logging.getLogger(__name__)


def generate_bim_geometry(
    db: Session, 
    project_id: str, 
    model_id: str, 
    element_ids: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Generate BIM geometry for elements.
    """
    try:
        # Get elements
        query = db.query(Element).filter(Element.project_id == project_id)
        if element_ids:
            query = query.filter(Element.id.in_(element_ids))
        elements = query.all()
        
        # Generate geometry for each element
        geometries = []
        
        for element in elements:
            # Get element properties
            start_node = db.query(Node).filter(Node.id == element.start_node_id).first()
            end_node = db.query(Node).filter(Node.id == element.end_node_id).first()
            section = db.query(Section).filter(Section.id == element.section_id).first()
            material = db.query(Material).filter(Material.id == element.material_id).first()
            
            if not start_node or not end_node or not section or not material:
                continue
            
            # Generate geometry based on element type
            if element.element_type in [ElementType.BEAM, ElementType.COLUMN, ElementType.BRACE]:
                geometry = _generate_linear_element_geometry(element, start_node, end_node, section)
            elif element.element_type == ElementType.TRUSS:
                geometry = _generate_truss_element_geometry(element, start_node, end_node, section)
            elif element.element_type == ElementType.PLATE:
                geometry = _generate_plate_element_geometry(element, db)
            elif element.element_type == ElementType.SHELL:
                geometry = _generate_shell_element_geometry(element, db)
            elif element.element_type == ElementType.SOLID:
                geometry = _generate_solid_element_geometry(element, db)
            else:
                # Default to simple line representation
                geometry = {
                    "element_id": element.id,
                    "geometry_type": element.element_type,
                    "vertices": [
                        [start_node.x, start_node.y, start_node.z],
                        [end_node.x, end_node.y, end_node.z]
                    ],
                    "edges": [[0, 1]],
                    "color": _get_material_color(material),
                    "properties": {
                        "name": element.name,
                        "section": section.name,
                        "material": material.name
                    }
                }
            
            # Add to geometries list
            if geometry:
                geometry["project_id"] = project_id
                geometry["bim_model_id"] = model_id
                geometries.append(geometry)
        
        return geometries
    
    except Exception as e:
        logger.error(f"Error generating BIM geometry: {str(e)}")
        return []


def _generate_linear_element_geometry(
    element: Element, 
    start_node: Node, 
    end_node: Node, 
    section: Section
) -> Dict[str, Any]:
    """
    Generate geometry for linear elements (beams, columns, braces).
    """
    # Get section dimensions
    dimensions = section.dimensions or {}
    
    # Default dimensions if not available
    h = dimensions.get("h", 200)  # Height/depth
    b = dimensions.get("b", 100)  # Width/flange width
    tw = dimensions.get("tw", 10)  # Web thickness
    tf = dimensions.get("tf", 15)  # Flange thickness
    
    # Calculate direction vector
    dx = end_node.x - start_node.x
    dy = end_node.y - start_node.y
    dz = end_node.z - start_node.z
    length = np.sqrt(dx**2 + dy**2 + dz**2)
    
    if length < 1e-6:
        return None
    
    # Normalize direction vector
    nx = dx / length
    ny = dy / length
    nz = dz / length
    
    # Calculate perpendicular vectors
    # First perpendicular vector (local y-axis)
    if abs(nz) < 0.9:  # Not vertical
        # Use cross product with global z-axis
        yx = -ny
        yy = nx
        yz = 0
    else:
        # Use cross product with global x-axis
        yx = 0
        yy = -nz
        yz = ny
    
    # Normalize
    y_length = np.sqrt(yx**2 + yy**2 + yz**2)
    yx /= y_length
    yy /= y_length
    yz /= y_length
    
    # Second perpendicular vector (local z-axis) using cross product
    zx = ny * yz - nz * yy
    zy = nz * yx - nx * yz
    zz = nx * yy - ny * yx
    
    # Apply rotation angle
    if element.angle != 0:
        angle_rad = np.radians(element.angle)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        
        # Rotate y and z axes
        yx_new = yx * cos_a + zx * sin_a
        yy_new = yy * cos_a + zy * sin_a
        yz_new = yz * cos_a + zz * sin_a
        
        zx = zx * cos_a - yx * sin_a
        zy = zy * cos_a - yy * sin_a
        zz = zz * cos_a - yz * sin_a
        
        yx, yy, yz = yx_new, yy_new, yz_new
    
    # Generate vertices based on section type
    vertices = []
    faces = []
    
    if section.section_type == SectionType.I:
        # I-section (H-section)
        # Generate 8 vertices for top flange
        h_half = h / 2
        b_half = b / 2
        
        # Top flange corners
        vertices.append([
            start_node.x + yx * (-b_half) + zx * h_half,
            start_node.y + yy * (-b_half) + zy * h_half,
            start_node.z + yz * (-b_half) + zz * h_half
        ])
        vertices.append([
            start_node.x + yx * b_half + zx * h_half,
            start_node.y + yy * b_half + zy * h_half,
            start_node.z + yz * b_half + zz * h_half
        ])
        vertices.append([
            end_node.x + yx * b_half + zx * h_half,
            end_node.y + yy * b_half + zy * h_half,
            end_node.z + yz * b_half + zz * h_half
        ])
        vertices.append([
            end_node.x + yx * (-b_half) + zx * h_half,
            end_node.y + yy * (-b_half) + zy * h_half,
            end_node.z + yz * (-b_half) + zz * h_half
        ])
        
        # Bottom flange corners
        vertices.append([
            start_node.x + yx * (-b_half) + zx * (-h_half),
            start_node.y + yy * (-b_half) + zy * (-h_half),
            start_node.z + yz * (-b_half) + zz * (-h_half)
        ])
        vertices.append([
            start_node.x + yx * b_half + zx * (-h_half),
            start_node.y + yy * b_half + zy * (-h_half),
            start_node.z + yz * b_half + zz * (-h_half)
        ])
        vertices.append([
            end_node.x + yx * b_half + zx * (-h_half),
            end_node.y + yy * b_half + zy * (-h_half),
            end_node.z + yz * b_half + zz * (-h_half)
        ])
        vertices.append([
            end_node.x + yx * (-b_half) + zx * (-h_half),
            end_node.y + yy * (-b_half) + zy * (-h_half),
            end_node.z + yz * (-b_half) + zz * (-h_half)
        ])
        
        # Web corners (if needed for detailed representation)
        # For simplicity, we'll use the flanges to define the faces
        
        # Define faces (6 faces for the box)
        faces = [
            [0, 1, 2, 3],  # Top flange top face
            [4, 5, 6, 7],  # Bottom flange bottom face
            [0, 3, 7, 4],  # Left side
            [1, 2, 6, 5],  # Right side
            [0, 1, 5, 4],  # Start cap
            [3, 2, 6, 7]   # End cap
        ]
        
        # Add web face
        web_width = tw
        web_y = 0  # Web is centered
        
        # Web vertices
        web_vertices_count = len(vertices)
        vertices.append([
            start_node.x + yx * (web_y - web_width/2) + zx * h_half,
            start_node.y + yy * (web_y - web_width/2) + zy * h_half,
            start_node.z + yz * (web_y - web_width/2) + zz * h_half
        ])
        vertices.append([
            start_node.x + yx * (web_y + web_width/2) + zx * h_half,
            start_node.y + yy * (web_y + web_width/2) + zy * h_half,
            start_node.z + yz * (web_y + web_width/2) + zz * h_half
        ])
        vertices.append([
            start_node.x + yx * (web_y + web_width/2) + zx * (-h_half),
            start_node.y + yy * (web_y + web_width/2) + zy * (-h_half),
            start_node.z + yz * (web_y + web_width/2) + zz * (-h_half)
        ])
        vertices.append([
            start_node.x + yx * (web_y - web_width/2) + zx * (-h_half),
            start_node.y + yy * (web_y - web_width/2) + zy * (-h_half),
            start_node.z + yz * (web_y - web_width/2) + zz * (-h_half)
        ])
        
        vertices.append([
            end_node.x + yx * (web_y - web_width/2) + zx * h_half,
            end_node.y + yy * (web_y - web_width/2) + zy * h_half,
            end_node.z + yz * (web_y - web_width/2) + zz * h_half
        ])
        vertices.append([
            end_node.x + yx * (web_y + web_width/2) + zx * h_half,
            end_node.y + yy * (web_y + web_width/2) + zy * h_half,
            end_node.z + yz * (web_y + web_width/2) + zz * h_half
        ])
        vertices.append([
            end_node.x + yx * (web_y + web_width/2) + zx * (-h_half),
            end_node.y + yy * (web_y + web_width/2) + zy * (-h_half),
            end_node.z + yz * (web_y + web_width/2) + zz * (-h_half)
        ])
        vertices.append([
            end_node.x + yx * (web_y - web_width/2) + zx * (-h_half),
            end_node.y + yy * (web_y - web_width/2) + zy * (-h_half),
            end_node.z + yz * (web_y - web_width/2) + zz * (-h_half)
        ])
        
        # Web faces
        faces.append([web_vertices_count + 0, web_vertices_count + 1, web_vertices_count + 5, web_vertices_count + 4])
        faces.append([web_vertices_count + 2, web_vertices_count + 3, web_vertices_count + 7, web_vertices_count + 6])
        faces.append([web_vertices_count + 1, web_vertices_count + 2, web_vertices_count + 6, web_vertices_count + 5])
        faces.append([web_vertices_count + 3, web_vertices_count + 0, web_vertices_count + 4, web_vertices_count + 7])
    
    elif section.section_type in [SectionType.RECTANGULAR, SectionType.SQUARE]:
        # Rectangular or square section
        h_half = h / 2
        b_half = b / 2
        
        # Top corners
        vertices.append([
            start_node.x + yx * (-b_half) + zx * h_half,
            start_node.y + yy * (-b_half) + zy * h_half,
            start_node.z + yz * (-b_half) + zz * h_half
        ])
        vertices.append([
            start_node.x + yx * b_half + zx * h_half,
            start_node.y + yy * b_half + zy * h_half,
            start_node.z + yz * b_half + zz * h_half
        ])
        vertices.append([
            end_node.x + yx * b_half + zx * h_half,
            end_node.y + yy * b_half + zy * h_half,
            end_node.z + yz * b_half + zz * h_half
        ])
        vertices.append([
            end_node.x + yx * (-b_half) + zx * h_half,
            end_node.y + yy * (-b_half) + zy * h_half,
            end_node.z + yz * (-b_half) + zz * h_half
        ])
        
        # Bottom corners
        vertices.append([
            start_node.x + yx * (-b_half) + zx * (-h_half),
            start_node.y + yy * (-b_half) + zy * (-h_half),
            start_node.z + yz * (-b_half) + zz * (-h_half)
        ])
        vertices.append([
            start_node.x + yx * b_half + zx * (-h_half),
            start_node.y + yy * b_half + zy * (-h_half),
            start_node.z + yz * b_half + zz * (-h_half)
        ])
        vertices.append([
            end_node.x + yx * b_half + zx * (-h_half),
            end_node.y + yy * b_half + zy * (-h_half),
            end_node.z + yz * b_half + zz * (-h_half)
        ])
        vertices.append([
            end_node.x + yx * (-b_half) + zx * (-h_half),
            end_node.y + yy * (-b_half) + zy * (-h_half),
            end_node.z + yz * (-b_half) + zz * (-h_half)
        ])
        
        # Define faces (6 faces for the box)
        faces = [
            [0, 1, 2, 3],  # Top face
            [4, 5, 6, 7],  # Bottom face
            [0, 3, 7, 4],  # Left side
            [1, 2, 6, 5],  # Right side
            [0, 1, 5, 4],  # Start cap
            [3, 2, 6, 7]   # End cap
        ]
    
    elif section.section_type == SectionType.CIRCULAR:
        # Circular section
        radius = dimensions.get("d", 100) / 2  # Diameter/2
        segments = 16  # Number of segments for the circle
        
        # Generate vertices for start cap
        for i in range(segments):
            angle = 2 * np.pi * i / segments
            x_offset = radius * np.cos(angle)
            z_offset = radius * np.sin(angle)
            
            # Transform to global coordinates
            vertices.append([
                start_node.x + yx * x_offset + zx * z_offset,
                start_node.y + yy * x_offset + zy * z_offset,
                start_node.z + yz * x_offset + zz * z_offset
            ])
        
        # Generate vertices for end cap
        for i in range(segments):
            angle = 2 * np.pi * i / segments
            x_offset = radius * np.cos(angle)
            z_offset = radius * np.sin(angle)
            
            # Transform to global coordinates
            vertices.append([
                end_node.x + yx * x_offset + zx * z_offset,
                end_node.y + yy * x_offset + zy * z_offset,
                end_node.z + yz * x_offset + zz * z_offset
            ])
        
        # Define faces
        # Start cap
        start_cap = list(range(segments))
        faces.append(start_cap)
        
        # End cap
        end_cap = list(range(segments, 2 * segments))
        faces.append(end_cap)
        
        # Side faces
        for i in range(segments):
            next_i = (i + 1) % segments
            faces.append([i, next_i, next_i + segments, i + segments])
    
    else:
        # Default to simple line representation for unsupported section types
        vertices = [
            [start_node.x, start_node.y, start_node.z],
            [end_node.x, end_node.y, end_node.z]
        ]
        edges = [[0, 1]]
        faces = []
    
    return {
        "element_id": element.id,
        "geometry_type": element.element_type,
        "vertices": vertices,
        "faces": faces,
        "edges": [] if faces else [[0, 1]],
        "color": _get_element_color(element),
        "properties": {
            "name": element.name,
            "section": section.name,
            "section_type": section.section_type,
            "dimensions": dimensions
        }
    }


def _generate_truss_element_geometry(
    element: Element, 
    start_node: Node, 
    end_node: Node, 
    section: Section
) -> Dict[str, Any]:
    """
    Generate geometry for truss elements.
    """
    # For trusses, we'll use a simplified representation
    # similar to beams but with smaller dimensions
    return _generate_linear_element_geometry(element, start_node, end_node, section)


def _generate_plate_element_geometry(
    element: Element, 
    db: Session
) -> Dict[str, Any]:
    """
    Generate geometry for plate elements.
    """
    # This would require getting all nodes associated with the plate element
    # and generating the appropriate geometry
    # For now, we'll return a placeholder
    return None


def _generate_shell_element_geometry(
    element: Element, 
    db: Session
) -> Dict[str, Any]:
    """
    Generate geometry for shell elements.
    """
    # This would require getting all nodes associated with the shell element
    # and generating the appropriate geometry
    # For now, we'll return a placeholder
    return None


def _generate_solid_element_geometry(
    element: Element, 
    db: Session
) -> Dict[str, Any]:
    """
    Generate geometry for solid elements.
    """
    # This would require getting all nodes associated with the solid element
    # and generating the appropriate geometry
    # For now, we'll return a placeholder
    return None


def _get_element_color(element: Element) -> str:
    """
    Get color for an element based on its type.
    """
    if element.element_type == ElementType.BEAM:
        return "#4285F4"  # Blue
    elif element.element_type == ElementType.COLUMN:
        return "#34A853"  # Green
    elif element.element_type == ElementType.BRACE:
        return "#FBBC05"  # Yellow
    elif element.element_type == ElementType.TRUSS:
        return "#EA4335"  # Red
    elif element.element_type == ElementType.PLATE:
        return "#9C27B0"  # Purple
    elif element.element_type == ElementType.SHELL:
        return "#FF9800"  # Orange
    elif element.element_type == ElementType.SOLID:
        return "#795548"  # Brown
    else:
        return "#9E9E9E"  # Grey


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