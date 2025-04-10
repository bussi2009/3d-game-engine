import tkinter as tk
from tkinter import ttk

class DraggableTab(ttk.Frame):
    def __init__(self, parent, title, content):
        super().__init__(parent)
        self.title = title
        self.content = content
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        
    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def on_drag(self, event):
        x = self.winfo_x() + (event.x - self.start_x)
        y = self.winfo_y() + (event.y - self.start_y)
        self.place(x=x, y=y)
        
    def on_release(self, event):
        self.place_forget()
        target = self.winfo_containing(event.x_root, event.y_root)
        if isinstance(target, TabbedPane):
            target.add_tab(self.title, self.content)

class TabbedPane(ttk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = title
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        
    def add_tab(self, title, content=None):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        if content:
            content.pack(in_=frame, expand=True, fill=tk.BOTH)
        return frame

class UnityLayout:
    def __init__(self, root):
        self.root = root
        self.root.title("Layout")
        self.root.geometry("1000x700")
        self.panes = {}
        self.setup_layout()
        
    def setup_layout(self):
        # Main vertical container
        main_vertical = tk.PanedWindow(self.root, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=8)
        main_vertical.pack(expand=True, fill=tk.BOTH)

        # Main horizontal container
        main_horizontal = tk.PanedWindow(main_vertical, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=8)
        
        # Left panel (Code blocks)
        left_pane = TabbedPane(main_horizontal, "Code blocks")
        self.panes['project'] = left_pane
        left_pane.add_tab("Code blocks", self.create_content("Code Block 1 Content"))

        # Center panel (Code)
        center_pane = TabbedPane(main_horizontal, "Code")
        self.panes['CodeMenu'] = center_pane
        center_pane.add_tab("Main Code", self.create_content("Code Editor Content"))

        # Right panel (Scene View)
        right_pane = TabbedPane(main_horizontal, "Scene View")
        self.panes['scene_view'] = right_pane
        right_pane.add_tab("3D View", self.create_content("Scene View Content"))

        # Add panels to main horizontal
        main_horizontal.add(left_pane, minsize=200)
        main_horizontal.add(center_pane, minsize=400)
        main_horizontal.add(right_pane, minsize=600)

        # Bottom panel (Project Files)
        bottom_pane = TabbedPane(main_vertical, "Project Files")
        self.panes['project_files'] = bottom_pane
        bottom_pane.add_tab("Files", self.create_content("Project Files Content"))

        # Add main sections to vertical container
        main_vertical.add(main_horizontal, minsize=500)
        main_vertical.add(bottom_pane, minsize=150)

    def create_content(self, text):
        frame = ttk.Frame()
        tk.Label(frame, 
                text=text, 
                bg="#1E1E1E", 
                fg="#858585", 
                font=('Helvetica', 12)
                ).pack(expand=True, fill=tk.BOTH)
        return frame

if __name__ == "__main__":
    root = tk.Tk()
    app = UnityLayout(root)
    root.mainloop()