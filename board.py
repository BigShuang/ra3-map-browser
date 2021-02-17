import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import os
import json

from constants import *
from logic import get_page_maps


class MapBoard(tk.Frame):
    def __init__(self, master, map_path, img_size, max_width, cr):
        super().__init__(master)
        self.map_path = map_path
        self.img_size = img_size
        self.max_width = max_width
        self.c = cr[0]
        self.r = cr[1]

        self.img_list = [None for _ in range(self.r * self.c)]
        self.label_list = [None for _ in range(self.r * self.c)]
        self.text_list = [None for _ in range(self.r * self.c)]
        self.page_info = get_page_maps(self.map_path, page=0, nums=self.r * self.c)

        self.vars = {}

    def bind_vars(self, **kwargs):
        for key in kwargs:
            self.vars[key] = kwargs[key]

    def refresh_with_setting(self, **kwargs):
        """
        :param kwargs: dict, keys:map_path, img_size, max_width, cr
        """
        if "map_path" in kwargs:
            self.map_path = kwargs["map_path"]
        if "img_size" in kwargs:
            self.img_size = kwargs["img_size"]
        if "max_width" in kwargs:
            self.max_width = kwargs["max_width"]
        if "cr" in kwargs:
            self.c, self.r = kwargs["cr"]

        lst = self.grid_slaves()
        for l in lst:
            l.destroy()

        self.img_list = [None for _ in range(self.r * self.c)]
        self.label_list = [None for _ in range(self.r * self.c)]
        self.text_list = [None for _ in range(self.r * self.c)]
        self.page_info = get_page_maps(self.map_path, page=0, nums=self.r * self.c)
        self.show_page_by_index(0)


    def refresh_vars(self):
        if "page_index" in self.vars:
            pi_str = "%s / %s" % (self.page_info["page"] + 1, self.page_info["pages"])
            self.vars["page_index"].set(pi_str)

        if "nums_count" in self.vars:
            self.vars["nums_count"].set(self.page_info["total"])

        if "left_button" in self.vars:
            if self.page_info.get("prev"):
                self.vars["left_button"].config(state=tk.NORMAL)
            else:
                self.vars["left_button"].config(state=tk.DISABLED)

        if "right_button" in self.vars:
            if self.page_info.get("next"):
                self.vars["right_button"].config(state=tk.NORMAL)
            else:
                self.vars["right_button"].config(state=tk.DISABLED)

        if "show_info" in self.vars:
            if os.path.exists(self.map_path):
                self.vars["show_info"].set("")
            else:
                self.vars["show_info"].set("你的地图文件夹不存在或已丢失")

    def show_page_by_index(self, index):
        if os.path.exists(self.map_path):
            self.page_info = get_page_maps(self.map_path, page=index, nums=self.r * self.c)
        else:
            self.page_info = {}
        for i in range(self.r * self.c):
            ri = i // self.c
            ci = i % self.c

            if i < len(self.page_info["maps"]):
                map_info = self.page_info["maps"][i]
                if "art_tga" in map_info:
                    self.img_list[i] = Image.open(map_info["art_tga"])
                elif "tga" in map_info:
                    self.img_list[i] = Image.open(map_info["tga"])
                else:
                    self.img_list[i] = Image.new("RGB", self.img_size, (0, 0, 0))

                self.img_list[i] = self.img_list[i].resize(self.img_size)
                self.img_list[i] = ImageTk.PhotoImage(self.img_list[i])

                if self.label_list[i] is None:
                    self.label_list[i] = tk.Label(self, image=self.img_list[i])
                    self.label_list[i].grid(row=ri * 2, column=ci)
                    self.label_list[i].bind("<Double-Button-1>", lambda e, i=i: self.click_map(i))
                else:
                    self.label_list[i].config(image=self.img_list[i])

                if self.text_list[i] is None:
                    self.text_list[i] = tk.Label(self, text=map_info["map"][:self.max_width], width=self.max_width)
                    self.text_list[i].grid(row=ri * 2 + 1, column=ci)
                else:
                    self.text_list[i].config(text=map_info["map"][:self.max_width])
            else:
                self.img_list[i] = Image.new("RGB", self.img_size, BLANK)
                self.img_list[i] = ImageTk.PhotoImage(self.img_list[i])

                if self.label_list[i] is None:
                    self.label_list[i] = tk.Label(self, image=self.img_list[i])
                    self.label_list[i].grid(row=ri * 2, column=ci)
                    self.label_list[i].bind("<Double-Button-1>", lambda e, i=i: self.click_map(i))
                else:
                    self.label_list[i].config(image=self.img_list[i])

                if self.text_list[i] is None:
                    self.text_list[i] = tk.Label(self, text="", width=self.max_width)
                    self.text_list[i].grid(row=ri * 2 + 1, column=ci)
                else:
                    self.text_list[i].config(text="")


        self.refresh_vars()

    def click_map(self, index):
        if "maps" in self.page_info and index <len(self.page_info["maps"]):
            map_info = self.page_info["maps"][index]
            subprocess.Popen(r'explorer /select,"%s"' % map_info["dir"])

    def prev_page(self):
        if self.page_info.get("prev"):
            prev_index = self.page_info["page"] - 1
            self.show_page_by_index(prev_index)

    def next_page(self):
        if self.page_info.get("next"):
            next_index = self.page_info["page"] + 1
            self.show_page_by_index(next_index)


class MainBoard(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.setting = {}
        self.vars = {}

    def set_setting(self, **setting):
        """
        :param setting: dict, keys: map_path, size, cr
        """
        self.setting.update(setting)


    def set_vars(self, **vars):
        """
        :param vars: dict, keys: font_2, page_index, show_info, nums_count
        """
        self.vars.update(vars)

    def refresh(self):
        self.map_board.refresh_with_setting(
            map_path=self.setting["map_path"], img_size=IMG_SIZE[self.setting["size"]],
            max_width=MAX_WIDTH[self.setting["size"]], cr=self.setting["cr"])

    def init(self):
        frame_top = tk.Frame(self)
        frame_top.grid(row=0)
        tk.Label(frame_top, text="双击地图图片，即可在文件浏览器中打开地图文件夹", font=self.vars["font_2"]).grid()
        tk.Label(frame_top, textvariable=self.vars["show_info"], font=self.vars["font_2"], fg="#FF69B4").grid()

        self.map_board = MapBoard(self, self.setting["map_path"], IMG_SIZE[self.setting["size"]],
                              MAX_WIDTH[self.setting["size"]], self.setting["cr"])
        self.map_board.show_page_by_index(0)
        self.map_board.grid(row=1)

        frame_bottom = tk.Frame(self)
        frame_bottom.grid(row=2)

        left_button = ttk.Button(frame_bottom, text="上一页", command=self.map_board.prev_page)
        page_label = tk.Label(frame_bottom, text="当前页面: ")
        page_i_label = tk.Label(frame_bottom, textvariable=self.vars["page_index"])
        page_label2 = tk.Label(frame_bottom, text="总地图数量: ")
        nums_label = tk.Label(frame_bottom, textvariable=self.vars["nums_count"])
        right_button = ttk.Button(frame_bottom, text="下一页", command=self.map_board.next_page)

        left_button.grid(row=0, column=0)
        page_label.grid(row=0, column=1)
        page_i_label.grid(row=0, column=2, padx=10)
        page_label2.grid(row=0, column=3)
        nums_label.grid(row=0, column=4, padx=10)
        right_button.grid(row=0, column=5)

        self.map_board.bind_vars(page_index=self.vars["page_index"], left_button=left_button, right_button=right_button,
                            show_info=self.vars["show_info"], nums_count=self.vars["nums_count"])
        self.map_board.refresh_vars()

        self.master.bind('<Left>', lambda e: self.map_board.prev_page())
        self.master.bind('<Right>', lambda e: self.map_board.next_page())


class SettingBoard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.init_done = False

        self.local_vars = {}
        self.local_vars["r"] = tk.IntVar(self, 0)
        self.local_vars["c"] = tk.IntVar(self, 0)
        self.local_vars["size"] = tk.StringVar(self, "S")

    def read_setting(self, main_board):
        self.local_vars["mb"] = main_board
        self.local_vars["size"].set(main_board.setting["size"])
        self.local_vars["c"].set(main_board.setting["cr"][0])
        self.local_vars["r"].set(main_board.setting["cr"][1])

    def set_vars(self, **vars):
        """
        :param vars: dict, keys: map_path(StringVar), setting_info(StringVar)
        """
        self.vars = vars

    def init(self):
        ROW1 = tk.Frame(self)
        ROW2 = tk.Frame(self)
        ROW3 = tk.Frame(self)
        ROW1.pack()
        ROW2.pack()
        ROW3.pack()
        label0 = ttk.Label(ROW1, textvariable=self.vars["st_info"], foreground="red")
        label0.grid(row=0, columnspan=2, pady=10)

        b0 = ttk.Button(ROW1, text="修改地图文件夹", command=self.select_dir)
        b0.grid(row=1, column=0)

        label_1 = ttk.Entry(ROW1, textvariable=self.vars["map_path"], state="disabled", width=80)
        label_1.grid(row=1, column=1, columnspan=2)

        ttk.Label(ROW2, text="行数：").grid(row=0, column=0)
        ttk.Label(ROW2, text="列数：").grid(row=1, column=0)

        tk.Scale(ROW2, from_=ROW_RANGE[0], to=ROW_RANGE[1], variable=self.local_vars["r"], orient='horizontal',
                 length=RANGE_WIDTH * (ROW_RANGE[1] - ROW_RANGE[0])).grid(row=0, column=1, columnspan=3)
        tk.Scale(ROW2, from_=COLUMN_RANGE[0], to=COLUMN_RANGE[1], variable=self.local_vars["c"], orient='horizontal',
                 length=RANGE_WIDTH * (COLUMN_RANGE[1] - COLUMN_RANGE[0])).grid(row=1, column=1, columnspan=3, padx=10)

        ttk.Label(ROW2, textvariable=self.local_vars["r"]).grid(row=0, column=4)
        ttk.Label(ROW2, textvariable=self.local_vars["c"]).grid(row=1, column=4)

        ttk.Label(ROW2, text="图片大小：").grid(row=2, column=0, padx=10, pady=10)
        tk.Radiobutton(ROW2, text="小", variable=self.local_vars["size"], value="S", width=7,
                       indicatoron=False).grid(row=2, column=1)
        tk.Radiobutton(ROW2, text="中", variable=self.local_vars["size"], value="M", width=7,
                       indicatoron=False).grid(row=2, column=2)
        tk.Radiobutton(ROW2, text="大", variable=self.local_vars["size"], value="L", width=7,
                       indicatoron=False).grid(row=2, column=3)

        tk.Button(self, text="保存并退出", command=self.save).pack(pady=10)
        tk.Button(self, text="返回", command=self.back).pack(pady=10)
        self.init_done = True

    def save(self):
        map_path = self.vars["map_path"].get()
        c = self.local_vars["c"].get()
        r = self.local_vars["r"].get()
        size = self.local_vars["size"].get()
        self.pack_forget()

        data = {
            "size": size,
            "c": c,
            "r": r
        }

        with open(JSON_NAME, "w") as f:
            json.dump(data, f)

        self.local_vars["mb"].set_setting(map_path=map_path, size=size, cr=(c, r))
        self.local_vars["mb"].refresh()

        self.local_vars["mb"].pack()

    def back(self):
        self.pack_forget()
        self.local_vars["mb"].pack()

    def select_dir(self):
        try:
            dir = filedialog.askdirectory()
            if dir:
                self.vars["map_path"].set(dir)
                print(dir)

            self.vars["st_info"].set("")
        except Exception as e:
            self.vars["st_info"].set(str(e))

def open_setting(gvars):
    gvars["mb"].pack_forget()
    gvars["sb"].read_setting(gvars["mb"])
    if not gvars["sb"].init_done:
        gvars["sb"].init()
    gvars["sb"].pack()
