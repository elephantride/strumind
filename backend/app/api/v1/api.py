from fastapi import APIRouter

from app.api.v1.endpoints import (
    projects,
    nodes,
    elements,
    materials,
    sections,
    loads,
    analysis,
    design,
    bim,
    detailing,
)

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(nodes.router, prefix="/nodes", tags=["nodes"])
api_router.include_router(elements.router, prefix="/elements", tags=["elements"])
api_router.include_router(materials.router, prefix="/materials", tags=["materials"])
api_router.include_router(sections.router, prefix="/sections", tags=["sections"])
api_router.include_router(loads.router, prefix="/loads", tags=["loads"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(design.router, prefix="/design", tags=["design"])
api_router.include_router(bim.router, prefix="/bim", tags=["bim"])
api_router.include_router(detailing.router, prefix="/detailing", tags=["detailing"])