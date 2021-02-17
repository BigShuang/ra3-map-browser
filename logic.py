import os
import math
import json
import datetime
from constants import SIZE, CR, IMG_SIZE, ROW_RANGE, COLUMN_RANGE

def get_all_maps(map_path):
    maps = []
    dirs = os.listdir(map_path)
    # print(len(dirs))
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
        "next": (page+1)*nums < len(all_maps),
        "total": len(all_maps)
    }
    return page_info


def get_map_path():
    map_relative_path = "AppData\Roaming\Red Alert 3\Maps"
    home = os.path.expanduser('~')
    map_path = os.path.join(home, map_relative_path)
    return map_path


def get_setting(setting_path):
    if os.path.exists(setting_path):
        try:
            with open(setting_path, "r") as f:
                data = json.load(f)
            if "size" in data and "c" in data and "r" in data:
                size = data["size"]
                c = data["c"]
                r = data["r"]
                if size in IMG_SIZE and ROW_RANGE[0] <= r <= ROW_RANGE[1]\
                        and COLUMN_RANGE[0] <= c <= COLUMN_RANGE[1]:
                    return size, (c, r)

        except Exception as e:
            print(e)
            log_time = datetime.datetime.now()
            log_str = str(log_time)
            for c in "- :.":
                log_str = log_str.replace(c, "_")
            with open("log_%s.txt"%log_str, "w") as f:
                f.write("get_setting errors:\n")
                f.write(str(e))

    return SIZE, CR


if __name__ == '__main__':
    map_path = get_map_path()
    # print(r)
    pass
    res = get_all_maps(map_path)


