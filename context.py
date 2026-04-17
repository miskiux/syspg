from dataclasses import dataclass
import logging

from manager import DatabaseManager
from env import db_dsn
from logger import setup_logger


@dataclass(frozen=True)
class Context:
    db: DatabaseManager
    logger: logging.Logger

def bootstrap_context() -> Context:
    return Context(
        db=DatabaseManager(db_dsn),
        logger=setup_logger()
    )