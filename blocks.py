# blocks.py
class Block:
    def __init__(self, block_type, params=None, children=None):
        self.block_type = block_type
        self.params = params or {}
        self.children = children or []
        self.uuid = id(self)
        
    def generate_code(self):
        raise NotImplementedError
    
    def draw(self, canvas):
        raise NotImplementedError

class MoveBlock(Block):
    def __init__(self, direction, distance):
        super().__init__(
            "move",
            params={"direction": direction, "distance": distance}
        )
    
    def draw(self, canvas):
        canvas.create_polygon(
            5, 20,
            15, 5,
            115, 5,
            115, 45,
            5, 45,
            5, 20,
            fill="#4A90D9", outline="white"
        )
        canvas.create_text(
            60, 25,
            text=f"Move {self.params['direction']} {self.params['distance']}",
            fill="white"
        )

class LoopBlock(Block):
    def __init__(self, iterations):
        super().__init__(
            "loop",
            params={"iterations": iterations}
        )
    
    def draw(self, canvas):
        canvas.create_polygon(
            5, 5,
            115, 5,
            115, 45,
            75, 45,
            75, 65,
            5, 65,
            5, 45,
            fill="#FFAB1D", outline="white"
        )
        canvas.create_text(
            60, 25,
            text=f"Loop {self.params['iterations']} times",
            fill="white"
        )
        canvas.create_rectangle(
            5, 45,
            75, 65,
            fill="", outline="white"
        )

class BlockPalette:
    def __init__(self):
        self.blocks = {
            'motion': [MoveBlock("forward", 10), MoveBlock("up", 10)],
            'control': [LoopBlock(4)]
        }
    
    def get_block_categories(self):
        return list(self.blocks.keys())