import logging

from sqlalchemy.exc import SQLAlchemyError

from app.db.session import Base, engine
from app.models import (
    node,
    element,
    material,
    section,
    load,
    analysis,
    design,
    project,
)

logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    """
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {e}")
        raise