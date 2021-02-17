import tkinter as tk
import os
import tkinter.ttk as ttk
from board import MainBoard, SettingBoard, open_setting
import tkinter.font as tkFont
import webbrowser

from logic import get_map_path, get_setting

from constants import *

MAP_PATH = get_map_path()
size, cr = get_setting(JSON_NAME)

win = tk.Tk()
win.title("ra3 map browser")

if os.path.exists(ICON_PATH):
    win.iconbitmap(ICON_PATH)

win.resizable(width=False, height=False)

def_font = tk.font.nametofont("TkDefaultFont")
font_2 = def_font.copy()
font_2.config(size=22)

page_index = tk.StringVar(win, "1")
nums_count = tk.IntVar(win, 0)
show_info = tk.StringVar(win, "")
# for frame 2
map_path = tk.StringVar(win, value=MAP_PATH)
setting_info = tk.StringVar(win, value="")

main_board = MainBoard(win)
main_board.pack()

gvars = {}

setting_board = SettingBoard(win)
setting_board.set_vars(map_path=map_path, st_info=setting_info)

gvars["sb"] = setting_board
gvars["mb"] = main_board

def view_author(event=None):
    webbrowser.open("https://space.bilibili.com/149259132")

def view_project(event=None):
    webbrowser.open("https://github.com/BigShuang/ra3-map-browser")

try:
    main_board.set_setting(map_path=MAP_PATH, size=size, cr=cr)
    main_board.set_vars(font_2=font_2, page_index=page_index, show_info=show_info, nums_count=nums_count)
    main_board.init()

    menu = tk.Menu(win)
    win.config(menu=menu)

    menu.add_cascade(label="设置", command=lambda : open_setting(gvars))
    menu.add_separator()
    menu.add_cascade(label="查看作者", command=view_author)
    menu.add_cascade(label="查看项目", command=view_project)

except Exception as e:
    show_info.set(str(e))

win.mainloop()