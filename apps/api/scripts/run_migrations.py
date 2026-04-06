"""Alembic migration scripts."""

import logging
from pathlib import Path

from alembic import command
from alembic.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_migrations() -> None:
    """Run Alembic migrations for persistent databases."""
    try:
        logger.info("Running database migrations...")
        alembic_cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error("Failed to run database migrations: %s", e)


if __name__ == "__main__":
    run_migrations()
