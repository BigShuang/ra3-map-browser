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

if ICON_PATH and os.path.exists(ICON_PATH):
    win.iconbitmap(ICON_PATH)

win.resizable(width=False, height=False)


def_font = tk.font.nametofont("TkDefaultFont")
font_1 = def_font.copy()
font_1.config(size=20)


vars ={
    "page_index" : tk.StringVar(win, "1"),
    "nums_count" : tk.IntVar(win, 0),
    "show_info" : tk.StringVar(win, ""),
    # for frame 2
    "map_path" : tk.StringVar(win, value=MAP_PATH),
    "setting_info" : tk.StringVar(win, value=""),

    "search_word": tk.StringVar(win, value=""),
    "kind_selector": tk.StringVar(win, value=SUGGEST[0]),

    "search_val": ""
}


main_board = MainBoard(win)
main_board.pack()

gvars = {}

setting_board = SettingBoard(win)
setting_board.set_vars(vars)

gvars["sb"] = setting_board
gvars["mb"] = main_board

def view_author(event=None):
    webbrowser.open("https://space.bilibili.com/149259132")

def view_project(event=None):
    webbrowser.open("https://github.com/BigShuang/ra3-map-browser")

if True:
# try:
    main_board.set_setting(map_path=MAP_PATH, size=size, cr=cr, font_1=font_1)
    main_board.set_vars_main(vars)
    main_board.init()

    menu = tk.Menu(win)
    win.config(menu=menu)

    menu.add_cascade(label="设置", command=lambda : open_setting(gvars))
    menu.add_separator()
    menu.add_cascade(label="查看作者", command=view_author)
    menu.add_cascade(label="查看项目", command=view_project)

# except Exception as e:
#     print(e)
#     vars["show_info"].set(str(e))

win.mainloop()