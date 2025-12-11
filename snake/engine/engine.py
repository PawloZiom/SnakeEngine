"""
Core Game Engine
Main engine loop and lifecycle management
"""

import logging
import time
from typing import Optional

from .window import Window


class Engine:
    """Main game engine with game loop"""
    
    def __init__(self, width: int = 1280, height: int = 720, title: str = "Snake Engine"):
        """
        Initialize engine
        
        Args:
            width: Window width
            height: Window height
            title: Window title
        """
        self.name = "Snake Engine"
        self.version = "0.1.0-alpha"
        self.logger = logging.getLogger("Engine")
        
        # Window and timing
        self.window: Optional[Window] = None
        self.target_fps = 60
        self.delta_time = 0.0
        self.frame_count = 0
        self.fps = 0.0
        
        # Window config
        self.window_width = width
        self.window_height = height
        self.window_title = title
        
        # State
        self.is_running = False
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def initialize(self) -> bool:
        """
        Initialize engine and window
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"Initializing {self.name} {self.version}")
        
        # Create window
        self.window = Window(
            width=self.window_width,
            height=self.window_height,
            title=self.window_title
        )
        
        if not self.window.create():
            self.logger.error("Failed to create window")
            return False
        
        self.logger.info("Engine initialized successfully")
        return True
    
    def run(self) -> None:
        """Run main game loop"""
        if not self.initialize():
            return
        
        self.is_running = True
        self.logger.info("Starting game loop")
        
        # Timing
        last_frame_time = time.time()
        fps_timer = time.time()
        fps_counter = 0
        
        # Main game loop
        while not self.window.should_close() and self.is_running:
            # Calculate delta time
            current_time = time.time()
            self.delta_time = current_time - last_frame_time
            last_frame_time = current_time
            
            # Update
            self._update()
            
            # Render
            self._render()
            
            # Update window
            self.window.update()
            
            # FPS counter
            fps_counter += 1
            elapsed = current_time - fps_timer
            if elapsed >= 1.0:
                self.fps = fps_counter / elapsed
                self.logger.debug(f"FPS: {self.fps:.1f}")
                fps_counter = 0
                fps_timer = current_time
            
            self.frame_count += 1
        
        self.shutdown()
    
    def _update(self) -> None:
        """Update game logic"""
        # TODO: Update entities, physics, etc.
        pass
    
    def _render(self) -> None:
        """Render frame"""
        # TODO: Clear screen and render
        pass
    
    def shutdown(self) -> None:
        """Shutdown engine and cleanup"""
        self.logger.info("Shutting down engine")
        
        if self.window:
            self.window.destroy()
        
        self.is_running = False
        self.logger.info(f"Engine shutdown (total frames: {self.frame_count})")