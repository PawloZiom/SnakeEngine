"""
Simple Demo - Snake Engine Window Test
Shows engine initialization and main loop
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from snake.engine import Engine, debug


def main():
    """Run simple demo"""
    print("=" * 60)
    print("Snake Engine - Simple Demo")
    print("=" * 60)
    print("\nControls:")
    print("  ESC - Close window")
    print("\nStarting engine...\n")
    
    # Create and run engine
    engine = Engine(
        width=1280,
        height=720,
        title="Snake Engine - Demo"
    )
    
    engine.run()
    
    debug.info("Demo finished successfully")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
