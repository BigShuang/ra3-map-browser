import tkinter as tk
from PIL import Image, ImageTk
from logic import get_page_maps
import subprocess
import os

# COLORS
BLANK = (220, 220, 220)

class MAP_BOARD(tk.Frame):
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

    def refresh_vars(self):
        if "page_index" in self.vars:
            pi_str = "%s / %s" % (self.page_info["page"] + 1, self.page_info["pages"])
            self.vars["page_index"].set(pi_str)

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

                ri = i // self.c
                ci = i % self.c

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


