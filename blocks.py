import tkinter as tk
from tkinter import ttk
class Block:
    def __init__(self, block_type, params=None, shape="rect"):
        self.block_type = block_type
        self.params = params or {}
        self.shape = shape
        self.color = "#4A90D9"
        self.children = []
        
    def get_label(self):
        return f"{self.block_type} block"
    
    def can_connect_top(self):
        return True
        
    def can_connect_bottom(self):
        return True
    
    def has_input_fields(self):
        return False
    
    def create_input_fields(self, canvas, x, y):
        pass


class MotionBlock(Block):
    def __init__(self, direction="forward", distance=10):
        super().__init__("move", {"direction": direction, "distance": distance}, "c-shaped")
        self.color = "#4A90D9"
        
    def get_label(self):
        return f"move {self.params['direction']}"
    
    def has_input_fields(self):
        return True
    
    def create_input_fields(self, canvas, x, y):
        self.distance_var = tk.StringVar(value=str(self.params['distance']))
        validate_cmd = (canvas.register(self.validate_motion_input), '%P')
        self.distance_entry = tk.Entry(
            canvas,
            textvariable=self.distance_var,
            width=5,
            validate="key",
            validatecommand=validate_cmd,
            bg="white",
            fg="black",
            bd=1,
            relief="sunken"
        )
        canvas.create_window(x+100, y+30, window=self.distance_entry)
    
    def validate_motion_input(self, new_val):
        try:
            if new_val == "" or new_val == "-":
                return True
            float(new_val)
            return True
        except ValueError:
            return False


class LoopBlock(Block):
    def __init__(self, times=4):
        super().__init__("repeat", {"times": times}, "hat")
        self.color = "#FFAB1D"
        
    def get_label(self):
        return "repeat"
    
    def can_connect_top(self):
        return False
    
    def has_input_fields(self):
        return True
    
    def create_input_fields(self, canvas, x, y):
        self.times_var = tk.StringVar(value=str(self.params['times']))
        validate_cmd = (canvas.register(self.validate_loop_input), '%P')
        self.times_entry = tk.Entry(
            canvas,
            textvariable=self.times_var,
            width=3,
            validate="key",
            validatecommand=validate_cmd,
            bg="white",
            fg="black",
            bd=1,
            relief="sunken"
        )
        canvas.create_window(x+60, y+30, window=self.times_entry)
    
    def validate_loop_input(self, new_val):
        return new_val.isdigit() or new_val == ""


class BlockPalette:
    def __init__(self):
        self.blocks = {
            "motion": [
                MotionBlock(direction="forward"),
                MotionBlock(direction="backward"),
            ],
            "control": [
                LoopBlock(times=4),
            ],
        }

    def get_block_categories(self):
        return self.blocks.keys()