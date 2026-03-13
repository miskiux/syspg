from dataclasses import dataclass
import logging

from manager import DatabaseManager
from env import db_url
from logger import setup_logger


@dataclass(frozen=True)
class Context:
    db_mgr: DatabaseManager
    logger: logging.Logger

def bootstrap_context() -> Context:
    return Context(
        db_mgr=DatabaseManager(db_url),
        logger=setup_logger()
    )