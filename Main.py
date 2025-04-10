import tkinter as tk
from main_window import ScratchEditor

if __name__ == "__main__":
    root = tk.Tk()
    app = ScratchEditor(root)
    root.mainloop()