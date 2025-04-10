import tkinter as tk
from tkinter import ttk

class BlockTemplate(tk.Canvas):
    def __init__(self, parent, block, editor, *args, **kwargs):
        super().__init__(
            parent,
            width=160,
            height=60,
            bg="#E0E0E0",
            bd=0,
            highlightthickness=0,
            *args, **kwargs
        )
        self.block = block
        self.editor = editor
        self.draw_block()
        self.bind("<ButtonPress-1>", self.on_press)
        
    def draw_block(self):
        self.delete("all")
        if self.block.shape == "rect":
            self.draw_rect_block()
        elif self.block.shape == "c-shaped":
            self.draw_c_shaped_block()
        elif self.block.shape == "hat":
            self.draw_hat_block()
        
        if self.block.has_input_fields():
            self.block.create_input_fields(self, 10, 10)
    
    def draw_rect_block(self):
        points = [5,5, 155,5, 155,55, 5,55, 5,5]
        self.create_polygon(points, fill=self.block.color, outline="white")
        self.create_text(80, 30, text=self.block.get_label(), fill="white")
        
    def draw_c_shaped_block(self):
        points = [5,5, 155,5, 155,25, 135,25, 135,55, 5,55, 5,5]
        self.create_polygon(points, fill=self.block.color, outline="white")
        self.create_text(80, 30, text=self.block.get_label(), fill="white")
        
    def draw_hat_block(self):
        points = [5,5, 155,5, 155,25, 135,25, 135,55, 5,55, 5,5]
        self.create_polygon(points, fill=self.block.color, outline="white")
        self.create_text(80, 30, text=self.block.get_label(), fill="white")
        
    def on_press(self, event):
        self.editor.start_drag(self.block, event)


class WorkspaceBlock:
    def __init__(self, canvas, block, x=0, y=0):
        self.canvas = canvas
        self.block = block
        self.x = x
        self.y = y
        self.dragging = False
        self.connected_to = None
        self.child_blocks = []
        self.create_block()
        
    def create_block(self):
        self.id = self.canvas.create_polygon(
            self.get_shape_points(),
            fill=self.block.color,
            outline="white",
            tags=("block", f"block_{id(self)}")
        )
        
        self.text_id = self.canvas.create_text(
            self.x + 80, self.y + 30,
            text=self.block.get_label(),
            fill="white",
            tags=("block_text", f"block_{id(self)}")
        )
        
        if self.block.has_input_fields():
            self.block.create_input_fields(self.canvas, self.x, self.y)
        
        self.bind_events()
        
    def get_shape_points(self):
        if self.block.shape == "rect":
            return [
                self.x+5, self.y+5,
                self.x+155, self.y+5,
                self.x+155, self.y+55,
                self.x+5, self.y+55,
                self.x+5, self.y+5
            ]
        elif self.block.shape == "c-shaped":
            return [
                self.x+5, self.y+5,
                self.x+155, self.y+5,
                self.x+155, self.y+25,
                self.x+135, self.y+25,
                self.x+135, self.y+55,
                self.x+5, self.y+55,
                self.x+5, self.y+5
            ]
        elif self.block.shape == "hat":
            return [
                self.x+5, self.y+5,
                self.x+155, self.y+5,
                self.x+155, self.y+25,
                self.x+135, self.y+25,
                self.x+135, self.y+55,
                self.x+5, self.y+55,
                self.x+5, self.y+5
            ]
    
    def bind_events(self):
        self.canvas.tag_bind(f"block_{id(self)}", "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(f"block_{id(self)}", "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(f"block_{id(self)}", "<ButtonRelease-1>", self.end_drag)
        
    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.dragging = True
        self.canvas.tag_raise(self.id)
        self.canvas.tag_raise(self.text_id)
        
    def on_drag(self, event):
        if self.dragging:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            self.move(dx, dy)
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.coords(self.id, self.get_shape_points())
        self.canvas.coords(self.text_id, self.x + 80, self.y + 30)
        
    def end_drag(self, event):
        self.dragging = False
        self.snap_to_nearest()
        
    def snap_to_nearest(self):
        closest = None
        min_dist = float('inf')
        
        for block_id in self.canvas.find_withtag("block"):
            if block_id == self.id:
                continue
                
            coords = self.canvas.coords(block_id)
            bx = coords[0]
            by = coords[1]
            
            dist = ((self.x - bx) ** 2 + (self.y - by) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest = block_id
                
        if closest and min_dist < 30:
            coords = self.canvas.coords(closest)
            self.x = coords[0]
            self.y = coords[1] + 60
            self.canvas.coords(self.id, self.get_shape_points())
            self.canvas.coords(self.text_id, self.x + 80, self.y + 30)