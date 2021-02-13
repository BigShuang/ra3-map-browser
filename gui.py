import tkinter as tk
import tkinter.ttk as ttk
# pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
from board import MAP_BOARD
import tkinter.font as tkFont


MAP_PATH = r"C:\Users\Administrator\AppData\Roaming\Red Alert 3\Maps"
IMGSIZE = (250, 250)
MAXWIDTH = 20
CR = [5, 3]


win = tk.Tk()
win.title("ra3 map browser")

def_font = tk.font.nametofont("TkDefaultFont")
font_2 = def_font.copy()
font_2.config(size=22)

page_index = tk.StringVar(win, "1")

frame_top = tk.Frame(win)
frame_top.grid(row=0)
tk.Label(frame_top, text="双击地图图片，即可在文件浏览器中打开地图文件夹", font=font_2).grid()


map_board = MAP_BOARD(win, MAP_PATH, IMGSIZE, MAXWIDTH, CR)
map_board.show_page_by_index(0)
map_board.grid(row=1)

frame_bottom = tk.Frame(win)
frame_bottom.grid(row=2)

left_button = ttk.Button(frame_bottom, text="上一页", command=map_board.prev_page)
page_label = tk.Label(frame_bottom, text="当前页面: ")
page_i_label = tk.Label(frame_bottom, textvariable=page_index)
right_button = ttk.Button(frame_bottom, text="下一页", command=map_board.next_page)

left_button.grid(row=0, column=0)
page_label.grid(row=0, column=1)
page_i_label.grid(row=0, column=2, padx=10)
right_button.grid(row=0, column=3)

map_board.bind_vars(page_index=page_index, left_button=left_button, right_button=right_button)
map_board.refresh_vars()

win.bind('<Left>', lambda e: map_board.prev_page())
win.bind('<Right>', lambda e: map_board.next_page())

win.mainloop()