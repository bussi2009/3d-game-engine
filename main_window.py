import tkinter as tk
from tkinter import ttk
from blocks import BlockPalette
from block_widgets import BlockTemplate, WorkspaceBlock

class ScratchEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Scratch-like Block Editor")
        self.root.geometry("1200x800")
        
        self.block_palette = BlockPalette()
        self.workspace_blocks = []
        self.drag_data = {"item": None, "ghost": None}
        
        self.setup_ui()
        
    def setup_ui(self):
        main_pane = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_pane.pack(expand=True, fill=tk.BOTH)
        
        content_pane = tk.PanedWindow(main_pane, orient=tk.HORIZONTAL)
        
        self.palette_frame = tk.Frame(content_pane, bg="#E0E0E0")
        self.create_palette()
        content_pane.add(self.palette_frame, width=250)
        
        self.workspace_frame = tk.Frame(content_pane)
        self.workspace_canvas = tk.Canvas(
            self.workspace_frame,
            bg="#F0F0F0",
            scrollregion=(0, 0, 2000, 2000)
        )
        h_scroll = tk.Scrollbar(self.workspace_frame, orient=tk.HORIZONTAL)
        v_scroll = tk.Scrollbar(self.workspace_frame, orient=tk.VERTICAL)
        
        h_scroll.config(command=self.workspace_canvas.xview)
        v_scroll.config(command=self.workspace_canvas.yview)
        self.workspace_canvas.config(
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set)
        
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.workspace_canvas.pack(expand=True, fill=tk.BOTH)
        
        content_pane.add(self.workspace_frame, width=700)
        
        self.preview_frame = tk.Frame(content_pane, bg="#333333")
        content_pane.add(self.preview_frame, width=250)
        
        self.console = tk.Text(main_pane, bg="#2D2D2D", fg="#CCCCCC")
        main_pane.add(content_pane)
        main_pane.add(self.console, height=100)
        
        self.workspace_canvas.bind("<ButtonPress-1>", self.workspace_click)
    
    def create_palette(self):
        for i, category in enumerate(self.block_palette.get_block_categories()):
            ttk.Label(
                self.palette_frame,
                text=category.upper(),
                background="#E0E0E0",
                font=("Arial", 10, "bold")
            ).grid(row=i*10, column=0, sticky="w", padx=10, pady=(10, 2))
            
            for j, block in enumerate(self.block_palette.blocks[category]):
                template = BlockTemplate(self.palette_frame, block, self)
                template.grid(row=i*10+j+1, column=0, padx=10, pady=2, sticky="ew")
    
    def start_drag(self, block, event):
        self.drag_data["item"] = block
        self.create_ghost_block(event)
        
    def create_ghost_block(self, event):
        if self.drag_data["ghost"]:
            self.drag_data["ghost"].destroy()
            
        ghost = tk.Toplevel(self.root)
        ghost.wm_overrideredirect(True)
        ghost.attributes("-alpha", 0.8)
        
        canvas = tk.Canvas(
            ghost,
            width=160,
            height=60,
            bg=self.drag_data["item"].color,
            bd=0,
            highlightthickness=0)
        
        if self.drag_data["item"].shape == "rect":
            points = [5,5, 155,5, 155,55, 5,55, 5,5]
        elif self.drag_data["item"].shape == "c-shaped":
            points = [5,5, 155,5, 155,25, 135,25, 135,55, 5,55, 5,5]
        elif self.drag_data["item"].shape == "hat":
            points = [5,5, 155,5, 155,25, 135,25, 135,55, 5,55, 5,5]
            
        canvas.create_polygon(points, fill=self.drag_data["item"].color, outline="white")
        canvas.create_text(80, 30, text=self.drag_data["item"].get_label(), fill="white")
        canvas.pack()
        
        x = event.x_root - 80
        y = event.y_root - 30
        ghost.geometry(f"+{x}+{y}")
        
        self.drag_data["ghost"] = ghost
        self.workspace_canvas.bind("<Motion>", self.move_ghost)
        self.workspace_canvas.bind("<ButtonRelease-1>", self.drop_block)
        
    def move_ghost(self, event):
        if self.drag_data["ghost"]:
            x = event.x_root - 80
            y = event.y_root - 30
            self.drag_data["ghost"].geometry(f"+{x}+{y}")
            
    def drop_block(self, event):
        if self.drag_data["item"]:
            canvas_x = self.workspace_canvas.canvasx(event.x)
            canvas_y = self.workspace_canvas.canvasy(event.y)
            
            new_block = WorkspaceBlock(
                self.workspace_canvas,
                self.drag_data["item"],
                canvas_x - 80,
                canvas_y - 30)
            self.workspace_blocks.append(new_block)
            
            if self.drag_data["ghost"]:
                self.drag_data["ghost"].destroy()
                self.drag_data["ghost"] = None
                
            self.workspace_canvas.unbind("<Motion>")
            self.workspace_canvas.unbind("<ButtonRelease-1>")
            self.drag_data["item"] = None
    
    def workspace_click(self, event):
        clicked = self.workspace_canvas.find_withtag("current")
        if clicked:
            block_id = clicked[0]
            for block in self.workspace_blocks:
                if block.id == block_id or block.text_id == block_id:
                    block.start_drag(event)
                    break