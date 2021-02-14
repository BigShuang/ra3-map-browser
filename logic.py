import tkinter as tk
import os
import math
import platform
import subprocess

def get_all_maps(map_path):
    maps = []
    dirs = os.listdir(map_path)
    print(len(dirs))
    for dir in dirs:
        dir_path = os.path.join(map_path, dir)
        if os.path.isdir(dir_path):
            # print(dir)
            map_info = {}
            files = os.listdir(dir_path)
            for file in files:
                name, suffix = os.path.splitext(file)
                if suffix == ".map":
                    map_info["map"] = dir
                elif suffix == ".tga":
                    if name.endswith("_art"):
                        map_info["art_tga"] = os.path.join(dir_path, file)
                    else:
                        map_info["tga"] = os.path.join(dir_path, file)

            if "map" in map_info:

                map_info["dir"] = dir_path
                maps.append(map_info)

    return maps


def get_page_maps(map_path, page=0, nums=12):
    """
    得到界面某一页将要展示的地图信息
    :param page: 第几页
    :param nums: 每页展示地图数
    :return: page info. A dictionary
    """
    all_maps = get_all_maps(map_path)
    page_info = {
        "page": page,
        "pages": math.ceil(len(all_maps)/nums),
        "prev": page > 0,
        "maps": all_maps[page*nums:(page+1)*nums],
        "next": (page+1)*nums < len(all_maps)

    }
    return page_info


def get_map_path():
    map_relative_path = "AppData\Roaming\Red Alert 3\Maps"
    home = os.path.expanduser('~')
    map_path = os.path.join(home, map_relative_path)
    return map_path

if __name__ == '__main__':
    map_path = get_map_path()
    # print(r)
    pass
    res = get_all_maps(map_path)


