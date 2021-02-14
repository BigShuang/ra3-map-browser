import tkinter as tk
parent_widget = tk.Tk()
scale_widget = tk.Scale(parent_widget, from_=1, to=5, length=200,
                             orient=tk.HORIZONTAL)
scale_widget.set(3)
scale_widget.pack()

parent_widget.mainloop()