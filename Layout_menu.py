import tkinter as tk
from tkinter import ttk
from blocks import BlockPalette

class Layouts:
    def __init__(self, root):
        self.root = root
        self.root.title("Scratch-like Block Editor")
        self.root.geometry("1200x800")

        # Initialize components
        self.block_palette = BlockPalette()
        self.workspace_blocks = []  # Tracks blocks in the workspace
        self.drag_data = {"item": None}  # Tracks drag state
        self.init_ui()

    def init_ui(self):
        """Initialize the main UI layout"""
        # Main vertical container
        main_vertical = tk.PanedWindow(self.root, orient=tk.VERTICAL, sashwidth=8)
        main_vertical.pack(expand=True, fill=tk.BOTH)

        # Horizontal container (workspace + panels)
        main_horizontal = tk.PanedWindow(main_vertical, orient=tk.HORIZONTAL, sashwidth=8)

        # Left Panel - Block Palette
        self.palette_frame = tk.Frame(main_horizontal, bg="#E0E0E0")
        self.populate_palette()
        main_horizontal.add(self.palette_frame, width=250)

        # Center Panel - Workspace
        self.workspace_canvas = tk.Canvas(main_horizontal, bg="#1E1E1E", bd=0, highlightthickness=0)
        self.workspace_canvas.bind("<B1-Motion>", self.on_workspace_drag)
        self.workspace_canvas.bind("<ButtonRelease-1>", self.on_workspace_release)
        main_horizontal.add(self.workspace_canvas, width=700)

        # Right Panel - 3D Preview
        self.preview_canvas = tk.Canvas(main_horizontal, bg="#333333", bd=0, highlightthickness=0)
        main_horizontal.add(self.preview_canvas, width=250)

        # Bottom Panel - Console
        self.console = tk.Text(main_vertical, bg="#2D2D2D", fg="#CCCCCC", height=10, bd=0)
        main_vertical.add(main_horizontal)
        main_vertical.add(self.console, height=100)

    def populate_palette(self):
        """Populate the block palette with draggable block templates"""
        row = 0
        for category in self.block_palette.get_block_categories():
            # Add category label
            ttk.Label(
                self.palette_frame,
                text=category.upper(),
                background="#E0E0E0",
                font=("Arial", 10, "bold"),
            ).grid(row=row, column=0, sticky="w", padx=10, pady=(10, 2))
            row += 1

            # Add blocks in the category
            for block in self.block_palette.blocks[category]:
                template = BlockTemplate(self.palette_frame, block)
                template.bind("<ButtonPress-1>", self.start_template_drag)
                template.grid(row=row, column=0, padx=10, pady=2, sticky="ew")
                row += 1

    def start_template_drag(self, event):
        """Start dragging a block template from the palette"""
        template = event.widget
        self.drag_data["item"] = template.block
        self.create_ghost(template)

    def create_ghost(self, template):
        """Create a ghost block for dragging"""
        self.ghost = tk.Canvas(
            self.root,
            width=template.winfo_width(),
            height=template.winfo_height(),
            bg="#4E4E4E",
            bd=0,
            highlightthickness=0,
        )
        template.block.draw(self.ghost)
        self.ghost.place(x=self.root.winfo_pointerx(), y=self.root.winfo_pointery())

    def on_workspace_drag(self, event):
        """Handle dragging over the workspace"""
        if self.drag_data["item"]:
            self.ghost.place(x=event.x_root - 60, y=event.y_root - 25)

    def on_workspace_release(self, event):
        """Handle releasing a block in the workspace"""
        if self.drag_data["item"]:
            # Check if the release is within the workspace bounds
            x = self.workspace_canvas.winfo_rootx()
            y = self.workspace_canvas.winfo_rooty()
            w = self.workspace_canvas.winfo_width()
            h = self.workspace_canvas.winfo_height()

            if (
                event.x_root >= x
                and event.x_root <= x + w
                and event.y_root >= y
                and event.y_root <= y + h
            ):
                # Create a new block in the workspace
                block = self.drag_data["item"]
                new_block = WorkspaceBlock(self.workspace_canvas, block)
                new_block.place(event.x_root - x - 60, event.y_root - y - 25)
                self.workspace_blocks.append(new_block)

            # Cleanup
            self.drag_data["item"] = None
            self.ghost.destroy()


class BlockTemplate(tk.Canvas):
    """A draggable block template in the palette"""

    def __init__(self, parent, block):
        super().__init__(
            parent,
            width=120,
            height=50,
            bg="#E0E0E0",
            bd=0,
            highlightthickness=0,
        )
        self.block = block
        self.block.draw(self)


class WorkspaceBlock:
    """A block placed in the workspace"""

    def __init__(self, canvas, block):
        self.canvas = canvas
        self.block = block
        self.create_block()
        self.bind_events()

    def create_block(self):
        """Create the visual representation of the block"""
        self.canvas_block = tk.Canvas(
            self.canvas,
            width=120,
            height=50,
            bg="#2E2E2E",
            bd=0,
            highlightthickness=0,
        )
        self.block.draw(self.canvas_block)
        self.id = self.canvas.create_window(0, 0, window=self.canvas_block)

    def place(self, x, y):
        """Position the block on the workspace"""
        self.canvas.coords(self.id, x, y)

    def bind_events(self):
        """Bind drag-and-drop events"""
        self.canvas_block.bind("<ButtonPress-1>", self.start_drag)
        self.canvas_block.bind("<B1-Motion>", self.on_drag)
        self.canvas_block.bind("<ButtonRelease-1>", self.end_drag)

    def start_drag(self, event):
        """Start dragging the block"""
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.tag_raise(self.id)

    def on_drag(self, event):
        """Handle block dragging"""
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        x, y = self.canvas.coords(self.id)
        self.canvas.coords(self.id, x + dx, y + dy)
        self.start_x = event.x
        self.start_y = event.y

    def end_drag(self, event):
        """Handle drag end"""
        # Implement snapping or connection logic here
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = Layouts(root)
    root.mainloop()