"""
Logging Module for Python REST API
Provides structured logging with correlation IDs
"""
import logging
import sys
from contextvars import ContextVar
from typing import Optional
import uuid

# Context variable for correlation ID
correlation_id: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)

class CorrelationFilter(logging.Filter):
    """Filter that adds correlation ID to log records"""
    
    def filter(self, record):
        record.correlation_id = correlation_id.get() or str(uuid.uuid4())[:8]
        return True

def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure structured logging"""
    logger = logging.getLogger("api")
    logger.setLevel(getattr(logging, level.upper()))
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(correlation_id)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    handler.addFilter(CorrelationFilter())
    logger.addHandler(handler)
    
    return logger

def get_logger(name: str = "api") -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)

def set_correlation_id(corr_id: Optional[str] = None) -> str:
    """Set correlation ID for current context"""
    if corr_id is None:
        corr_id = str(uuid.uuid4())[:8]
    correlation_id.set(corr_id)
    return corr_id
