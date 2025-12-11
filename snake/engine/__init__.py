"""
Snake Engine Core package

Usage:
    from snake.engine import Engine, debug
    
    engine = Engine()
    engine.run()
    
    debug.info("Game started")
"""

from .engine import Engine
from . import debug

__all__ = ["Engine", "debug"]
