import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from SnakeEngine import SnakeEngine, GameScript

def main():
    engine = SnakeEngine()
    engine.Start()
    
class Test(GameScript):
    pass

if __name__ == '__main__':
    main()
